#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"


module add apps/python/3.7.3
[ -z "$DO_EXPERIMENT_1" ] || python $SCRIPT_MERGE $LOG_FOLDER_E1/
[ -z "$DO_EXPERIMENT_2" ] || python $SCRIPT_MERGE $LOG_FOLDER_E2/
[ -z "$DO_EXPERIMENT_3" ] || python $SCRIPT_MERGE $LOG_FOLDER_E3/
[ -z "$DO_EXPERIMENT_4" ] || python $SCRIPT_MERGE $LOG_FOLDER_E4/
[ -z "$DO_EXPERIMENT_5" ] || python $SCRIPT_MERGE $LOG_FOLDER_E5/
[ -z "$DO_EXPERIMENT_6" ] || python $SCRIPT_MERGE $LOG_FOLDER_E6/
[ -z "$DO_EXPERIMENT_7" ] || python $SCRIPT_MERGE $LOG_FOLDER_E7/

