#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_experiments.py

module add apps/python/3.7.3
[ -z "$DO_EXPERIMENT_1" ] || python $PLOT_EXPERIMENT $LOG_FOLDER/experiment1-traces/
[ -z "$DO_EXPERIMENT_2" ] || python $PLOT_EXPERIMENT $LOG_FOLDER/experiment2-singleMin/
[ -z "$DO_EXPERIMENT_3" ] || python $PLOT_EXPERIMENT $LOG_FOLDER/experiment3-singleSame/
[ -z "$DO_EXPERIMENT_4" ] || python $PLOT_EXPERIMENT $LOG_FOLDER/experiment4-extraAtFeeder/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment4-mazes/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-single/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-twoScales/