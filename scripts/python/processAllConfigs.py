import sys
from pythonUtils.VariableLoader import *

"""
   This file is to be called after processing each individual configuration
   The file merges all information, and processes inter configuration data
   Stores files:
        'runtimes.pickle'
            config . location . episode . rat . steps . normalized . mazeFile
        'summaries.pickle'
            config . location . episode . count . mean . std . min . 25% . 50% . 75% . max . mazeFile
        'summaries_normalized.pickle'
            config . location . episode . count . mean . std . min . 25% . 50% . 75% . max . mazeFile
        
"""


def process_all_configs(base_folder):
    # load configs
    config_folders = get_list_of_configs(base_folder)
    configs = load_config_file(base_folder)

    # load variables
    summaries = load_summaries(base_folder, config_folders)
    summaries_normalized = load_normalized_summaries(base_folder, config_folders)
    runtimes = load_runtimes(base_folder, config_folders)

    # add mazes to summaries:
    mazes = configs.loc[summaries['config']]['mazeFile']
    mazes.index = summaries.index
    summaries['mazeFile'] = mazes
    summaries_normalized['mazeFile'] = mazes

    print(configs.columns)

    # add mazes to runtimes
    mazes = configs.loc[runtimes['config']]['mazeFile']
    mazes.index = runtimes.index
    runtimes['mazeFile'] = mazes

    maze_data = configs[['mazeFile', 'numStartingPositions']].drop_duplicates().reset_index().drop(['config'], axis=1)
    print(maze_data)

    pd.to_pickle(runtimes, base_folder+'runtimes.pickle')
    pd.to_pickle(summaries, base_folder+'summaries.pickle')
    pd.to_pickle(summaries_normalized, base_folder+'summaries_normalized.pickle')

if __name__ == '__main__':
    process_all_configs(os.path.join(sys.argv[1], ''))
