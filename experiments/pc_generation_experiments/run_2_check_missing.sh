#!/bin/sh
#in git root folder execute the following commands:

source "experiments/pc_generation_experiments/run_set_variables.sh"

CHECK_FILE="r#ID-steps.bin"

for E in ${RUN[*]}; do
	echo "sh python $SCRIPT_2_CHECK $(map $E LOG_FOLDER) $CHECK_FILE"
	python $SCRIPT_2_CHECK $(map $E LOG_FOLDER) $CHECK_FILE

	num_missing=`awk -F ',' '{print NF}' $(map $E LOG_FOLDER)/missing.csv`
	if [ -z "$num_missing" ]; then
	    echo 'no missing'
	else
	    MIN_RAT=0
		MAX_RAT=`expr $num_missing - 1`
	    echo Running missing from $MIN_RAT to $MAX_RAT
		sh $SCRIPT_1_RUN_ALL $(map $E CONFIG_FILE) $(map $E LOG_FOLDER) $(map $E BATCH_SIZE) $MIN_RAT $MAX_RAT 'DO_MISSING'
	fi

done
