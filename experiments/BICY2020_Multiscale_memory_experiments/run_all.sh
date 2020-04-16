#in git root folder execute the following commands:

RUN_ALL="scripts/circe_cluster/run_all_batches.sh"
EXPERIMENT_FOLDER="experiments/BICY2020_Multiscale_memory_experiments/"
LOG_FOLDER="logs/BICY2020_redone/"

sh $RUN_ALL ${EXPERIMENT_FOLDER}/experiment1-Traces.csv ${LOG_FOLDER}experiment1-traces 100
sh $RUN_ALL ${EXPERIMENT_FOLDER}/experiment2-SingleMin.csv ${LOG_FOLDER}experiment2-singleMin 100
sh $RUN_ALL ${EXPERIMENT_FOLDER}/experiment3-SaingleSame.csv ${LOG_FOLDER}experiment3-singleSame 100
sh $RUN_ALL ${EXPERIMENT_FOLDER}/experiment4-Mazes.csv ${LOG_FOLDER}experiment4-mazes 100
sh $RUN_ALL ${EXPERIMENT_FOLDER}/experiment5-Single.csv ${LOG_FOLDER}experiment5-single 100
sh $RUN_ALL ${EXPERIMENT_FOLDER}/experiment5-TwoScales.csv ${LOG_FOLDER}experiment5-twoScales 100