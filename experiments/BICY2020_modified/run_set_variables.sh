#in git root folder execute the following commands:

# AUXILIARY FUNCTION
map() { eval "echo \${$1[$2]}"; }

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
RUN=()
RUN+=(E1)
#RUN+=(E2)
#RUN+=(E3)
#RUN+=(E4)
#RUN+=(E5)
#RUN+=(E6)
RUN+=(E7)

decalre -A E1=( ["NAME"]="experiment1-traces" )
decalre -A E2=( ["NAME"]="experiment2-singleMin" )
decalre -A E3=( ["NAME"]="experiment3-singleSame" )
decalre -A E4=( ["NAME"]="experiment4-extraAtFeeder" )
decalre -A E5=( ["NAME"]="experiment5-density" )
decalre -A E6=( ["NAME"]="experiment6-extraAtGap" )
decalre -A E7=( ["NAME"]="experiment7-nonUniform" )

# EXPERIMENT LOG FOLDERS
for E in $RUN[*]; do
	eval "$E[LOG_FOLDER]=\$LOG_FOLDER/\$(map $E NAME)"
	eval "$E[CONFIG_FILE]=\$CONFIGS_FOLDER/\$(map $E NAME).csv"

	echo $(map $E LOG_FOLDER)
	echo $(map $E CONFIG_FILE)

done

# E1[LOG_FOLDER]=$LOG_FOLDER/$E1
# E2[LOG_FOLDER]=$LOG_FOLDER/$E2
# E3[LOG_FOLDER]=$LOG_FOLDER/$E3
# E4[LOG_FOLDER]=$LOG_FOLDER/$E4
# E5[LOG_FOLDER]=$LOG_FOLDER/$E5
# E6[LOG_FOLDER]=$LOG_FOLDER/$E6
# E7[LOG_FOLDER]=$LOG_FOLDER/$E7

# EXPERIMENT CONFIG FILES
# E1[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E1 NAME).csv
# E2[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E2 NAME).csv
# E3[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E3 NAME).csv
# E4[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E4 NAME).csv
# E5[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E5 NAME).csv
# E6[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E6 NAME).csv
# E7[CONFIG_FILE]=$CONFIGS_FOLDER/$(map E7 NAME).csv



# DO_EXPERIMENT_1=1
# DO_EXPERIMENT_2=1
# DO_EXPERIMENT_3=1
# DO_EXPERIMENT_4=1
# DO_EXPERIMENT_5=1
# DO_EXPERIMENT_6=1
# DO_EXPERIMENT_7=1
