#in git root folder execute the following commands:

PLOT_EXPERIMENT="experiments/BICY2020_modified/post_processing/plot_experiments.py"
LOG_FOLDER="experiments/BICY2020_modified/logs/"
module add apps/python/3.7.3

# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment1-traces/
python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment2-singleMin/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment3-singleSame/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment4-mazes/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-single/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-twoScales/