#!/bin/sh
# This script starts slurm path plotting scripts and configuration processing scripts 

source "experiments/BICY2020_modified/run_set_variables.sh"

# slurm script for path plotting:clear
PATH_PLOT_SCRIPT="module add apps/python/3.7.3; echo config \$SLURM_ARRAY_TASK_ID; python $SCRIPT_3_PLOT_PATHS ENAME/ c\$SLURM_ARRAY_TASK_ID"

for E in ${RUN[*]}; do

	# num rats in experiment is number of lines in config file -2:
	numLines=`wc -l $(map $E CONFIG_FILE) | cut -f1 -d' '`
	numRats=$((${numLines} - 2))

	# if max and min rats were not defined, then define them
	[[ -z "$(map $E MIN_RAT)" ]] && MIN_RAT=0 || MIN_RAT=$(map $E MIN_RAT)
	[[ -z "$(map $E MAX_RAT)" ]] && MAX_RAT=$numRats || MAX_RAT=$(map $E MAX_RAT) 

	# if max and min configs were not defined, then define them
	[[ -z "$(map $E MIN_CONFIG)" ]] && MIN_CONFIG=$(config "$(map $E LOG_FOLDER)/configs.csv" "$MIN_RAT"  ) || MIN_CONFIG=$(map $E MIN_CONFIG)
	[[ -z "$(map $E MAX_CONFIG)" ]] && MAX_CONFIG=$(config "$(map $E LOG_FOLDER)/configs.csv" "$MAX_RAT"  ) || MAX_CONFIG=$(map $E MAX_CONFIG)

	if [ "${1,,}" == "serial" ]; then
		for c_id in $(seq $MIN_CONFIG $MAX_CONFIG)
		do
			SLURM_ARRAY_TASK_ID=$c_id
			echo "${PATH_PLOT_SCRIPT/ENAME/$(map $E LOG_FOLDER)}"
			eval "${PATH_PLOT_SCRIPT/ENAME/$(map $E LOG_FOLDER)}"

			echo "bash $SCRIPT_3_PROCESS_CONFIG $(map $E LOG_FOLDER)/ $(map $E SAMPLE_RATE) $c_id"
			bash $SCRIPT_3_PROCESS_CONFIG $(map $E LOG_FOLDER)/ $(map $E SAMPLE_RATE) c$c_id
		done
	else
		echo "sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap=\"${PATH_PLOT_SCRIPT/ENAME/$(map $E LOG_FOLDER)}\""
		sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${PATH_PLOT_SCRIPT/ENAME/$(map $E LOG_FOLDER)}"

		echo "sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} $SCRIPT_3_PROCESS_CONFIG $(map $E LOG_FOLDER)/ $(map $E SAMPLE_RATE)"
		sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} $SCRIPT_3_PROCESS_CONFIG $(map $E LOG_FOLDER)/ $(map $E SAMPLE_RATE)
	fi

done
