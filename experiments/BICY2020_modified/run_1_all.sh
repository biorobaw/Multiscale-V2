#!/bin/sh
#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"


for E in ${RUN[*]}; do

	# num rats in experiment is number of lines in config file -2:
	numLines=`wc -l $(map $E CONFIG_FILE) | cut -f1 -d' '`
	numRats=`expr ${numLines} - 2`

	# if not defined, define min and max rat to be executed
	[[ -z "$(map $E MIN_RAT)" ]] && MIN_RAT=0 || MIN_RAT=$(map $E MIN_RAT)
	[[ -z "$(map $E MAX_RAT)" ]] && MAX_RAT=$numRats || MAX_RAT=$(map $E MAX_RAT)  

	if [ "${1,,}" == "serial" ]; then
		echo "Serial, running rats: $MIN_RAT-$MAX_RAT $(map $E NAME)"
		source /home/p/pablos/bash_exports.txt

		# create log structure:
		python scripts/circe_cluster/logFolderGenerator.py $(map $E LOG_FOLDER) $(map $E CONFIG_FILE)

		CMD_ARGS="-cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar -Xmx1500m com.github.biorobaw.scs.Main"

		MINI_BATCH="$2"		
		[[ -z "$MINI_BATCH" ]] || LAST=$(( $MINI_BATCH - 1 ))
		for rat_id in $(seq $MIN_RAT $MAX_RAT)
		do
			echo "rat $rat_id"
			# Note: prepending "time -v" to command gives time and max memory usage of program + other metrics
			if [[ -z "$MINI_BATCH" ]]; then
				time -v java $CMD_ARGS $(map $E CONFIG_FILE) $rat_id $(map $E LOG_FOLDER) >> serial_out.out
				[ $? -eq 0 ] || FAILED_IDS="$FAILED_IDS, $rat_id"
			else
				java $CMD_ARGS $(map $E CONFIG_FILE) $rat_id $(map $E LOG_FOLDER) >> serial_out.out &
				# PIDS+=($!)

				# check if last job to commit, if it is, then wait
				if [[ "$(( $rat_id %  $MINI_BATCH ))" == "$LAST" || "$rat_id" == "$MAX_RAT" ]]; then
					echo "waiting"
					wait
				fi

			fi
			# check exit status
			

		done

		echo "Failed ids: $FAILED_IDS" >> serial_out.out
		echo "Failed ids: $FAILED_IDS"

	else
		echo "sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT"
		sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT
	fi
done
