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

	echo "sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT"
	sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT
done
