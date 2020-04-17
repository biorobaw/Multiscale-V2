#in git root folder execute the following commands:

CHECK="scripts/log_processing/pythonUtils/MissingFiles.py"
LOG_FOLDER="logs/BICY2020_redone/"
FILE="r#ID-steps.bin"

echo ""
echo "E1"
python $CHECK ${LOG_FOLDER}experiment1-traces/     $FILE

echo ""
echo "E2"
python $CHECK ${LOG_FOLDER}experiment2-singleMin/  $FILE

echo ""
echo "E3"
python $CHECK ${LOG_FOLDER}experiment3-singleSame/ $FILE

echo ""
echo "E4"
python $CHECK ${LOG_FOLDER}experiment4-mazes/      $FILE

echo ""
echo "E5-single"
python $CHECK ${LOG_FOLDER}experiment5-single/     $FILE

echo ""
echo "E5-two"
python $CHECK ${LOG_FOLDER}experiment5-twoScales/  $FILE