#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"
PROCESS_CONFIG="scripts/circe_cluster/configuration_process_results.sh"

[ -z "$DO_EXPERIMENT_1" ] || sbatch -a 0-139 $PROCESS_CONFIG $LOG_E1/ 5
[ -z "$DO_EXPERIMENT_2" ] || sbatch -a 0-27  $PROCESS_CONFIG $LOG_E2/ 1
[ -z "$DO_EXPERIMENT_3" ] || sbatch -a 0-27  $PROCESS_CONFIG $LOG_E3/
[ -z "$DO_EXPERIMENT_4" ] || sbatch -a 0-21  $PROCESS_CONFIG $LOG_E4/ 5
# sbatch -a 0-47 $PROCESS_CONFIG ${LOG_FOLDER}experiment4-mazes/
# sbatch -a 0-27 $PROCESS_CONFIG ${LOG_FOLDER}experiment5-single/
# sbatch -a 0-181 $PROCESS_CONFIG ${LOG_FOLDER}experiment5-twoScales/