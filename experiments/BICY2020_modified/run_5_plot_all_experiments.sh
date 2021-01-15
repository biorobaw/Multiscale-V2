#!/bin/sh
#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"



module add apps/python/3.7.3

for E in ${RUN[*]}; do
	echo "python $SCRIPT_4_MERGE $(map $E LOG_FOLDER)/ "
	python $SCRIPT_5_PLOT_EXPERIMENT $(map $E LOG_FOLDER)/ 
done

