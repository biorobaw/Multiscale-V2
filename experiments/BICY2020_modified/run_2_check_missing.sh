#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

CHECK_FILE="r#ID-steps.bin"

[ -z "$DO_EXPERIMENT_1" ] || ( echo "E1" && python $SCRIPT_CHECK $LOG_FOLDER_E1/ $CHECK_FILE 100 )
[ -z "$DO_EXPERIMENT_2" ] || ( echo "E2" && python $SCRIPT_CHECK $LOG_FOLDER_E2/ $CHECK_FILE 100 )
[ -z "$DO_EXPERIMENT_3" ] || ( echo "E3" && python $SCRIPT_CHECK $LOG_FOLDER_E3/ $CHECK_FILE 100 )
[ -z "$DO_EXPERIMENT_4" ] || ( echo "E4" && python $SCRIPT_CHECK $LOG_FOLDER_E4/ $CHECK_FILE 100 )
[ -z "$DO_EXPERIMENT_5" ] || ( echo "E5" && python $SCRIPT_CHECK $LOG_FOLDER_E5/ $CHECK_FILE 50 )
[ -z "$DO_EXPERIMENT_6" ] || ( echo "E6" && python $SCRIPT_CHECK $LOG_FOLDER_E6/ $CHECK_FILE 100 )
[ -z "$DO_EXPERIMENT_7" ] || ( echo "E7" && python $SCRIPT_CHECK $LOG_FOLDER_E7/ $CHECK_FILE 100 )

