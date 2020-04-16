#in git root folder execute the following commands:

RUN_ALL="scripts/circe_cluster/configuration_process_results.sh"
LOG_FOLDER="logs/BICY2020_redone/"

sbatch -a 0-139 $RUN_ALL ${LOG_FOLDER}experiment1-traces
sbatch -a 0-27 $RUN_ALL ${LOG_FOLDER}experiment2-singleMin
sbatch -a 0-27 $RUN_ALL ${LOG_FOLDER}experiment3-singleSame
sbatch -a 0-47 $RUN_ALL ${LOG_FOLDER}experiment4-mazes
sbatch -a 0-27 $RUN_ALL ${LOG_FOLDER}experiment5-single
sbatch -a 0-181 $RUN_ALL ${LOG_FOLDER}experiment5-twoScales