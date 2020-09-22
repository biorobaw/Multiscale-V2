#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

CHECK="scripts/log_processing/pythonUtils/MissingFiles.py"
FILE="r#ID-steps.bin"


[ -z "$DO_EXPERIMENT_1" ] || ( echo "E1" && python $CHECK $LOG_E1/ $FILE 100 )
[ -z "$DO_EXPERIMENT_2" ] || ( echo "E2" && python $CHECK $LOG_E2/ $FILE 100 )
[ -z "$DO_EXPERIMENT_3" ] || ( echo "E3" && python $CHECK $LOG_E3/ $FILE 100 )
[ -z "$DO_EXPERIMENT_4" ] || ( echo "E4" && python $CHECK $LOG_E4/ $FILE 100 )
[ -z "$DO_EXPERIMENT_5" ] || ( echo "E5" && python $CHECK $LOG_E5/ $FILE 50 )
[ -z "$DO_EXPERIMENT_6" ] || ( echo "E6" && python $CHECK $LOG_E6/ $FILE 100 )

# echo ""
# echo "E4"
# python $CHECK ${LOG_FOLDER}experiment4-mazes/      $FILE 100

# echo ""
# echo "E5-single"
# python $CHECK ${LOG_FOLDER}experiment5-single/     $FILE 100

# echo ""
# echo "E5-two"
# python $CHECK ${LOG_FOLDER}experiment5-twoScales/  $FILE 100