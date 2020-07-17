import sys
from pythonUtils.VariableLoader import *
import sqlite3
from shutil import copyfile


def merge_databases(base_folder):
    # note: we broke data frames based on starting location
    # in

    # load configs
    # base_folder = '../../experiments/BICY2020_modified/logs/experiment1-traces/'
    db_name_format = base_folder + '{}/config_results.sqlite'
    db_experiment_name = base_folder + 'experiment_results.sqlite'
    config_folders = get_list_of_configs(base_folder)
    # config_folders = ['c0', 'c0']

    # copy first config database and then open it
    copyfile(db_name_format.format(config_folders[0]), db_experiment_name)
    db_experiment = sqlite3.connect(db_experiment_name)
    cursor = db_experiment.cursor()

    # get name of all tables:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = cursor.fetchall()

    # append dbs from all other configs
    for config in config_folders[1:]:
        db_config_name = db_name_format.format(config)
        cursor.execute("ATTACH DATABASE ? AS merging", (db_config_name, ))

        for table in all_tables: # obs table is a tuple
            cursor.execute("INSERT INTO {} SELECT * FROM merging.{}".format(table[0], table[0]))

        db_experiment.commit()
        cursor.execute("DETACH DATABASE merging")



if __name__ == '__main__':
    merge_databases(os.path.join(sys.argv[1], ''))
