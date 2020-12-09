#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

PROCESS_ALL="scripts/log_processing/processAllConfigs.py"


module add apps/python/3.7.3
[ -z "$DO_EXPERIMENT_1" ] || python $PROCESS_ALL $LOG_E1/
[ -z "$DO_EXPERIMENT_2" ] || python $PROCESS_ALL $LOG_E2/
[ -z "$DO_EXPERIMENT_3" ] || python $PROCESS_ALL $LOG_E3/
[ -z "$DO_EXPERIMENT_4" ] || python $PROCESS_ALL $LOG_E4/
[ -z "$DO_EXPERIMENT_5" ] || python $PROCESS_ALL $LOG_E5/
[ -z "$DO_EXPERIMENT_6" ] || python $PROCESS_ALL $LOG_E6/
[ -z "$DO_EXPERIMENT_7" ] || python $PROCESS_ALL $LOG_E7/
# python $PROCESS_ALL ${LOG_FOLDER}experiment4-mazes/
# python $PROCESS_ALL ${LOG_FOLDER}experiment5-single/
# python $PROCESS_ALL ${LOG_FOLDER}experiment5-twoScales/