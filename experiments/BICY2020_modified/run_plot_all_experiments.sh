#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_experiments.py

module add apps/python/3.7.3
[ -z "$DO_EXPERIMENT_1" ] || python $PLOT_EXPERIMENT $LOG_E1/
[ -z "$DO_EXPERIMENT_2" ] || python $PLOT_EXPERIMENT $LOG_E2/
[ -z "$DO_EXPERIMENT_3" ] || python $PLOT_EXPERIMENT $LOG_E3/
[ -z "$DO_EXPERIMENT_4" ] || python $PLOT_EXPERIMENT $LOG_E4/
[ -z "$DO_EXPERIMENT_5" ] || python $PLOT_EXPERIMENT $LOG_E5/
[ -z "$DO_EXPERIMENT_6" ] || python $PLOT_EXPERIMENT $LOG_E6/
[ -z "$DO_EXPERIMENT_7" ] || python $PLOT_EXPERIMENT $LOG_E7/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment4-mazes/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-single/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-twoScales/