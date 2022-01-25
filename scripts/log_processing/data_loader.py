import os
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
    configs['mazeFile'] = configs['mazeFile'].apply(os.path.basename)
    configs['config'] = configs['config'].apply(os.path.basename)
    return configs.set_index(['config'])


def load_summaries(db, config_indices, location):
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query("select config, location, episode, [50%] as steps "
                           "from rat_summaries_errors "
                           "where config in ({}) "
                           "AND location = {}"
                           .format(indices_str, np.uint8(location)), db)
    # adjust data types to reduce memory size
    df.config = df.config.astype(np.uint16)
    df.location = df.location.astype(np.uint8)
    df.episode = df.episode.astype(np.uint16)
    df.steps = df.steps.astype(np.float32)
    return df


def load_deltaV(db, config_indices, location):
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query("select config, location, episode, deltaV "
                           "from rat_summaries_normalized "
                           "where config in ({}) "
                           "AND location = {}"
                           .format(indices_str, np.uint8(location)), db)
    # adjust data types to reduce memory size
    df.config = df.config.astype(np.uint16)
    df.location = df.location.astype(np.uint8)
    df.episode = df.episode.astype(np.uint16)
    df.deltaV = df.deltaV.astype(np.float32)
    return df


def load_episode_runtimes(db, config_indices, location, episode):
    episode = np.uint16(episode)
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query("select config, location, rat, episode, errors as steps "
                           "from rat_runtimes "
                           "where episode={} "
                           "AND config in ({}) "
                           "AND location = {}"
                           .format(episode, indices_str, np.uint8(location)), db)
    # adjust data types to reduce memory size
    df.config = df.config.astype(np.uint16)
    df.location = df.location.astype(np.uint8)
    df.episode = df.episode.astype(np.uint16)
    df.steps = df.steps.astype(np.float32)
    return df

def load_all_runtimes_smaller_than_threshold(db, config_indices, location, threshold):
    indices_str = ','.join(map(str, config_indices))
    df = pd.read_sql_query(f"select config, location, rat, episode, errors as steps "
                           f"from rat_runtimes "
                           f"where config in ({indices_str}) "
                           f"AND location = {np.uint8(location)} "
                           f"AND errors < {threshold}"
                           , db)
    # adjust data types to reduce memory size
    df.config = df.config.astype(np.uint16)
    df.location = df.location.astype(np.uint8)
    df.episode = df.episode.astype(np.uint16)
    df.steps = df.steps.astype(np.float32)
    return df



