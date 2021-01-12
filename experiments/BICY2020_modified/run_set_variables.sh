#in git root folder execute the following commands:

# FOLDERS
EXPERIMENT_FOLDER="experiments/BICY2020_modified"
CONFIGS_FOLDER=$EXPERIMENT_FOLDER/config_files
LOG_FOLDER=$EXPERIMENT_FOLDER/logs

# SCRIPTS
SCRIPT_1_RUN_ALL="scripts/circe_cluster/run_all_batches.sh"
SCRIPT_2_CHECK="scripts/log_processing/pythonUtils/MissingFiles.py"
SCRIPT_3_PROCESS_CONFIG="scripts/circe_cluster/configuration_process_results.sh"
SCRIPT_3_PLOT_PATHS=$EXPERIMENT_FOLDER/post_processing/plot_paths.py
SCRIPT_4_MERGE="scripts/log_processing/mergeConfigs.py"
SCRIPT_5_PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_experiments.py

# EXPERIMENTS
E1=experiment1-traces
E2=experiment2-singleMin
E3=experiment3-singleSame
E4=experiment4-extraAtFeeder
E5=experiment5-density
E6=experiment6-extraAtGap
E7=experiment7-nonUniform

# EXPERIMENT LOG FOLDERS
LOG_FOLDER_E1=$LOG_FOLDER/$E1
LOG_FOLDER_E2=$LOG_FOLDER/$E2
LOG_FOLDER_E3=$LOG_FOLDER/$E3
LOG_FOLDER_E4=$LOG_FOLDER/$E4
LOG_FOLDER_E5=$LOG_FOLDER/$E5
LOG_FOLDER_E6=$LOG_FOLDER/$E6
LOG_FOLDER_E7=$LOG_FOLDER/$E7

# EXPERIMENT CONFIG FILES
CONFIG_FILE_E1=$CONFIGS_FOLDER/$E1.csv
CONFIG_FILE_E2=$CONFIGS_FOLDER/$E2.csv
CONFIG_FILE_E3=$CONFIGS_FOLDER/$E3.csv
CONFIG_FILE_E4=$CONFIGS_FOLDER/$E4.csv
CONFIG_FILE_E5=$CONFIGS_FOLDER/$E5.csv
CONFIG_FILE_E6=$CONFIGS_FOLDER/$E6.csv
CONFIG_FILE_E7=$CONFIGS_FOLDER/$E7.csv



# DO_EXPERIMENT_1=1
# DO_EXPERIMENT_2=1
# DO_EXPERIMENT_3=1
# DO_EXPERIMENT_4=1
# DO_EXPERIMENT_5=1
# DO_EXPERIMENT_6=1
DO_EXPERIMENT_7=1
