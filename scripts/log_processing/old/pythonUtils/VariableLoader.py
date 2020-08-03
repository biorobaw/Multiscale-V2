import pandas as pd
import os
import re
import numpy as np


def get_list_of_configs(configs_folder):
    all_configs = [f for f in os.listdir(configs_folder) if re.match('c\\d+$', f)]
    return sorted(all_configs, key = lambda x: int(x[1:]))


def get_list_of_mazes(base_folder):
    return [f for f in os.listdir(base_folder) if re.match('M\\d+.xml', f)]


def load_config_file(base_folder):
    configs = pd.read_csv(base_folder + 'configs.csv', sep='\t')
    configs = configs.drop(columns=['run_id']).drop_duplicates()
    configs['mazeFile'] = configs['mazeFile'].apply(os.path.basename)
    configs['config'] = configs['config'].apply(os.path.basename)
    return configs.set_index(['config'])


def load_config_variable(filename, base_folder, config_folders):
    df = pd.DataFrame()
    for c in config_folders:
        aux_frame = pd.read_pickle(base_folder + c + '/' + filename)
        aux_frame['config'] = int(c[1:])
        df = df.append(aux_frame)
    df.config = df.config.astype(np.uint16)
    return df


def load_runtimes(base_folder, configs_folders):
    return load_config_variable('configData.pickle', base_folder, configs_folders)


def load_normalized_summaries(base_folder, configs_folders):
    return load_config_variable('summaryNormalized.pickle', base_folder, configs_folders)


def load_summaries(base_folder, config_folders):
    return load_config_variable('summary.pickle', base_folder, config_folders)
