#in git root folder execute the following commands:

RUN_ALL="scripts/log_processing/processAllConfigs.py"
LOG_FOLDER="experiments/BICY2020_modified/logs/"

module add apps/python/3.7.3

python $RUN_ALL ${LOG_FOLDER}experiment1-traces/
python $RUN_ALL ${LOG_FOLDER}experiment2-singleMin/
python $RUN_ALL ${LOG_FOLDER}experiment3-singleSame/
# python $RUN_ALL ${LOG_FOLDER}experiment4-mazes/
# python $RUN_ALL ${LOG_FOLDER}experiment5-single/
# python $RUN_ALL ${LOG_FOLDER}experiment5-twoScales/