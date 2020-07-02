import sys
from pythonUtils.VariableLoader import *

"""
   This file is to be called after processing each individual configuration
   The file merges all information, and processes inter configuration data
   Stores files:
        'run_times_lN.pickle' = config . episode . rat . steps 
            run times for all configs, of all rats starting at location N. 
            When N=-1, results aggregate all locations
        
        'nrun_times_lN.pickle' = config . episode . rat . steps'
            Idem as before but using normalized data
        
        'run_times_summary_lN.pickle' : config . episode . count . mean . std . min . 25% . 50% . 75% . max
            result of aggregating rats and finding performance metrics
            
        'nrun_times_summary_lN.pickle' : episode . count . mean . std . min . 25% . 50% . 75% . max
            Idem to previous but with normalized results
        
"""


def process_all_configs(base_folder, location):
    # note: we broke data frames based on starting location
    # in

    # load configs
    config_folders = get_list_of_configs(base_folder)
    configs        = load_config_file(base_folder)

    # load summaries, normalized summaries, run times and normalized runtimes
    # note, we divided data frames into starting locations
    # usually we will just use the aggregated results (location=-1)
    # but the location can be modified using a console variable

    run_times_file = 'run_times_l{}.pickle'.format(location)
    summary_file   = 'run_times_summary_l{}.pickle'.format(location)
    files = [run_times_file, 'n' + run_times_file, summary_file, 'n' + summary_file]

    for file in files:
        df = load_config_variable(file, base_folder, config_folders)
        pd.to_pickle(df, base_folder + file)




    # add mazes to summaries:
    # mazes = configs.loc[summaries['config']]['mazeFile']
    # mazes.index = summaries.index
    # summaries['mazeFile'] = mazes
    # summaries_normalized['mazeFile'] = mazes

    # print(configs.columns)

    # add mazes to runtimes
    # mazes = configs.loc[runtimes['config']]['mazeFile']
    # mazes.index = runtimes.index
    # runtimes['mazeFile'] = mazes

    # maze_data = configs[['mazeFile', 'numStartingPositions']].drop_duplicates().reset_index().drop(['config'], axis=1)
    # print(maze_data)

    # pd.to_pickle(runtimes, base_folder+'runtimes.pickle')
    # pd.to_pickle(summaries, base_folder+'summaries.pickle')
    # pd.to_pickle(summaries_normalized, base_folder+'summaries_normalized.pickle')


if __name__ == '__main__':
    location = -1 if len(sys.argv) < 3 else int(sys.argv[2])
    process_all_configs(os.path.join(sys.argv[1], ''))
