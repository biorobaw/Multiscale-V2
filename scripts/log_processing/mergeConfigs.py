import sys
import sqlite3
from shutil import copyfile
import time
import tracemalloc
import os
from os.path import join as join_path
from data_loader import *

def merge_all_config_dbs(base_folder):
    # name format for condif and destination DBs
    configs_folder = join_path(base_folder, 'configs', '')
    db_name_format = configs_folder + '{}/config_results.sqlite'
    db_experiment_name = base_folder + 'experiment_results.sqlite'

    # create destination and get list of configs to merge:
    merge_configs = create_destination_and_get_DBs_to_append(db_experiment_name, configs_folder, db_name_format)

    # open destination database:
    db_experiment = sqlite3.connect(db_experiment_name)
    cursor = db_experiment.cursor()

    # get name of all tables:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = cursor.fetchall()

    for config in merge_configs:
        
        t2 = time.time()
        print('Merging config ', config, end =" " )
        db_config_name = db_name_format.format(config)
        cursor.execute("ATTACH DATABASE ? AS merging", (db_config_name, ))

        for table in all_tables: # obs table is a tuple
            table_name = table[0]
            if table_name != 'configs':
                cursor.execute(f"REPLACE INTO {table_name} SELECT * FROM merging.{table_name}")

        db_experiment.commit()
        cursor.execute("DETACH DATABASE merging")
        print(time.time() - t2)

    # save configs table to database
    configs = load_config_file(base_folder)
    configs = configs.reset_index()
    configs.config = configs.config.apply(lambda s: s[1:]).astype(int)
    configs.to_sql('configs', con=db_experiment, index=False, if_exists='replace')

    


def create_destination_and_get_DBs_to_append(db_experiment_name, configs_folder, db_name_format):

    """ Returns the list of DBs that have been modified since last merge.
        The function also creates the destination DB if it doesn't exist or if more
        than half of all config dbs have been modified since last merge.
    """

    # get the list of config names
    config_names = get_list_of_configs(configs_folder)

    # if destination file already exist find which configs have been modified since last merge
    destination_exists = os.path.exists(db_experiment_name)
    if destination_exists:
        # find last time the destination file was modified and all config dbs modified after that
        last_modified = os.stat(db_experiment_name).st_mtime
        modified_configs = [c for c in config_names if os.stat(db_name_format.format(c)).st_mtime > last_modified]

    else:
        # dbs have never been merged, all should be considered as modified
        modified_configs = config_names

    print('Total modified configs:', len(modified_configs))

    # if more than half of all databases have been modified, it will be faster to start over
    if len(modified_configs) >= 0.5 * len(config_names):
        print('Creating destination database...')

        # if destination exists delete it
        if destination_exists:
            os.remove(db_experiment_name)

        # init destination db by copying over first db in list
        copyfile(db_name_format.format(config_names[0]), db_experiment_name)

        # assume all configs (except the first) have been modified
        modified_configs = config_names[1:]

    return modified_configs








if __name__ == '__main__':
    tracemalloc.start()
    t1 = time.time()

    merge_all_config_dbs(os.path.join(sys.argv[1], ''))

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print('TOTAL TIME: {}'.format(time.time() - t1))
    print('MEMORY: current {}MB, peak {}MB'.format(current / 10 ** 6, peak / 10 ** 6))
