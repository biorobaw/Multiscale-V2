import sys
import sqlite3
from shutil import copyfile
import time
import tracemalloc
from os.path import join as join_path
from data_loader import *



def merge_databases(base_folder):
    tracemalloc.start()
    t1 = time.time()

    # load configs
    # base_folder = '../../experiments/BICY2020_modified/logs/experiment1-traces/'
    configs_folder = join_path(base_folder, 'configs', '')
    db_name_format = configs_folder + '{}/config_results.sqlite'
    db_experiment_name = base_folder + 'experiment_results.sqlite'
    config_names = get_list_of_configs(configs_folder)
    # config_names = ['c0', 'c0', 'c0', 'c0']

    # if database exist, delete it
    if os.path.exists(db_experiment_name):
        os.remove(db_experiment_name)

    # copy first config database and then open it
    copyfile(db_name_format.format(config_names[0]), db_experiment_name)
    db_experiment = sqlite3.connect(db_experiment_name)
    cursor = db_experiment.cursor()

    # get name of all tables:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = cursor.fetchall()

    # append dbs from all other configs
    for config in config_names[1:]:
        t2 = time.time()
        print('Merging config ', config, end =" " )
        db_config_name = db_name_format.format(config)
        cursor.execute("ATTACH DATABASE ? AS merging", (db_config_name, ))

        for table in all_tables: # obs table is a tuple
            cursor.execute("INSERT INTO {} SELECT * FROM merging.{}".format(table[0], table[0]))

        db_experiment.commit()
        print(time.time() - t2)
        cursor.execute("DETACH DATABASE merging")


    # add configs table to database
    configs = load_config_file(base_folder)
    configs = configs.reset_index()
    configs.config = configs.config.apply(lambda s: s[1:]).astype(int)
    configs.to_sql('configs', con=db_experiment, index=False)

    print('TOTAL TIME: {}'.format(time.time() - t1))
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print('MEMORY: current {}MB, peak {}MB'.format(current / 10 ** 6, peak / 10 ** 6))


if __name__ == '__main__':
    merge_databases(os.path.join(sys.argv[1], ''))
