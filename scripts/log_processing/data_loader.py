import os
import ntpath
import re
import numpy as np
import pandas as pd


def get_list_of_configs(configs_folder):
    all_configs = [f for f in os.listdir(configs_folder) if re.match('c\\d+$', f)]
    return sorted(all_configs, key=lambda x: int(x[1:]))


def get_list_of_mazes(mazes_folder):
    return [f for f in os.listdir(mazes_folder) if re.match('M\\d+.xml', f)]


def load_config_file(base_folder):
    configs = pd.read_csv(base_folder + 'configs.csv', sep='\t')
    configs = configs.drop(columns=['run_id']).drop_duplicates()
    configs['maze']   = configs.mazeFile.map(lambda v : ntpath.basename(v)[0:-4])
    configs['config'] = configs['config'].apply(os.path.basename)
    configs['c_id']   = configs.config.map(lambda v : int(v[1:]))
    return configs.set_index(['config'])


def load_summary_medians(db, config_indices, column):
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query("select config, episode, [50%] as median "
                           "from rat_summaries_{} "
                           "where config in ({})"
                           .format(column, indices_str), db)
    # adjust data types to reduce memory size
    df.config  = df.config.astype(np.uint16)
    df.episode = df.episode.astype(np.uint16)
    df['median']  = df['median'].astype(np.float32)
    return df


# def load_deltaV(db, config_indices, location):
#     indices_str = ','.join(map(str, config_indices))
#     df = pd.read_sql_query("select config, location, episode, deltaV "
#                            "from rat_summaries_normalized "
#                            "where config in ({}) "
#                            "AND location = {}"
#                            .format(indices_str, np.uint8(location)), db)
#     # adjust data types to reduce memory size
#     df.config = df.config.astype(np.uint16)
#     df.location = df.location.astype(np.uint8)
#     df.episode = df.episode.astype(np.uint16)
#     df.deltaV = df.deltaV.astype(np.float32)
#     return df


def load_episode_metrics(db, config_indices, episode):
    episode = np.uint16(episode)
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query("select config, episode, rat, steps, error_rate "
                           "from rat_episodic_metrics "
                           "where config in ({}) "
                           "AND episode={}"
                           .format(indices_str, episode), db)
    # adjust data types to reduce memory size
    df.config     = df.config.astype(np.uint16)
    df.episode    = df.episode.astype(np.uint16)
    df.rat        = df.rat.astype(np.uint8)
    df.steps      = df.steps.astype(np.float32)
    df.error_rate = df.error_rate.astype(np.float32)
    return df

def load_learning_times(db, config_indices):
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query("select config, rat, learning_time "
                           "from rat_metrics "
                           "where config in ({})"
                           .format(indices_str), db)
    # adjust data types to reduce memory size
    df.config     = df.config.astype(np.uint16)
    df.rat        = df.rat.astype(np.uint8)
    return df

# def load_all_runtimes_smaller_than_threshold(db, config_indices, location, threshold):
#     indices_str = ','.join(map(str, config_indices))
#     df = pd.read_sql_query(f"select config, location, rat, episode, errors as steps "
#                            f"from rat_runtimes "
#                            f"where config in ({indices_str}) "
#                            f"AND location = {np.uint8(location)} "
#                            f"AND errors < {threshold}"
#                            , db)
#     # adjust data types to reduce memory size
#     df.config = df.config.astype(np.uint16)
#     df.location = df.location.astype(np.uint8)
#     df.episode = df.episode.astype(np.uint16)
#     df.steps = df.steps.astype(np.float32)
#     return df



