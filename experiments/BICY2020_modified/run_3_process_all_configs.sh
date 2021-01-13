# This script starts slurm path plotting scripts and configuration processing scripts 

source "experiments/BICY2020_modified/run_set_variables.sh"

# slurm script for path plotting:
BATCH_SCRIPT="module add apps/python/3.7.3; python $SCRIPT_3_PLOT_PATHS ENAME/ c\$SLURM_ARRAY_TASK_ID"

for E in ${RUN[*]}; do

	# num rats in experiment is number of lines in config file -2:
	numLines=`wc -l $(map $E CONFIG_FILE) | cut -f1 -d' '`
	numRats=$((${numLines} - 2))

	# if max and min rats were not defined, then define them
	[[ -z "$(map $E MIN_RAT)" ]] && MIN_RAT=0 || MIN_RAT=$(map $E MIN_RAT)
	[[ -z "$(map $E MAX_RAT)" ]] && MAX_RAT=$numRats || MAX_RAT=$(map $E MAX_RAT) 

	# if max and min configs were not defined, then define them
	[[ -z "$(map $E MIN_CONFIG)" ]] && MIN_CONFIG=$(($MIN_RAT / $(map $E RATS))) || MIN_CONFIG=$(map $E MIN_CONFIG)
	[[ -z "$(map $E MAX_CONFIG)" ]] && MAX_CONFIG=$(($MAX_RAT / $(map $E RATS))) || MAX_CONFIG=$(map $E MAX_CONFIG)

	echo "sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap=\"${BATCH_SCRIPT/ENAME/$(map $E LOG_FOLDER)}\""
	sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$(map $E LOG_FOLDER)}"

	echo "sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} $SCRIPT_3_PROCESS_CONFIG $(map $E LOG_FOLDER)/ $(map $E SAMPLE_RATE)"
	sbatch -a ${MIN_CONFIG}-${MAX_CONFIG} $SCRIPT_3_PROCESS_CONFIG $(map $E LOG_FOLDER)/ $(map $E SAMPLE_RATE)

done
