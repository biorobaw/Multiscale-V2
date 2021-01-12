#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"


[ -z "$DO_EXPERIMENT_1" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E1 $LOG_FOLDER_E1 10
[ -z "$DO_EXPERIMENT_2" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E2 $LOG_FOLDER_E2 10
[ -z "$DO_EXPERIMENT_3" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E3 $LOG_FOLDER_E3  4
[ -z "$DO_EXPERIMENT_4" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E4 $LOG_FOLDER_E4 10
[ -z "$DO_EXPERIMENT_5" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E5 $LOG_FOLDER_E5  8
[ -z "$DO_EXPERIMENT_6" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E6 $LOG_FOLDER_E6 10
[ -z "$DO_EXPERIMENT_7" ] || sh $SCRIPT_RUN_ALL $CONFIG_FILE_E7 $LOG_FOLDER_E7 25
# sh $RUN_ALL ${CONFIG_FOLDER}/experiment4-Mazes.csv ${LOG_FOLDER}experiment4-mazes 100
# sh $RUN_ALL ${CONFIG_FOLDER}/experiment5-Single.csv ${LOG_FOLDER}experiment5-single 100
# sh $RUN_ALL ${CONFIG_FOLDER}/experiment5-TwoScales.csv ${LOG_FOLDER}experiment5-twoScales 100