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
		module add apps/jdk/11.0.5 
		module add apps/python/3.7.3;

		# create log structure:
		python scripts/circe_cluster/logFolderGenerator.py $(map $E LOG_FOLDER) $(map $E CONFIG_FILE)

		CMD_ARGS="-cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar -Xmx1500m com.github.biorobaw.scs.Main"
		for rat_id in $(seq $MIN_RAT $MAX_RAT)
		do
			echo "rat $rat_id"
			# Note: prepending "time -v" to command gives time and max memory usage of program + other metrics
			time -v java $CMD_ARGS $(map $E CONFIG_FILE) $rat_id $(map $E LOG_FOLDER) >> serial_out.out

			# check exit status
			[ $? -eq 0 ] || FAILED_IDS="$rat_id, $FAILED_IDS"

		done

		echo "Failed ids: $FAILED_IDS" >> serial_out.out
		echo "Failed ids: $FAILED_IDS"

	else
		echo "sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT"
		sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT
	fi
done
