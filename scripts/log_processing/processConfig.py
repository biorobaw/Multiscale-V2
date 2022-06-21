import glob
import sys
import numpy as np
from scipy import stats
from pythonUtils.BinaryFiles import *
from data_loader import *
import time
import sqlite3
from sqlite3 import Error
import tracemalloc


def create_db_and_tables(config_folder):
    # create database to store results (delete if it already exists)
    db_name = config_folder + 'config_results.sqlite'
    if os.path.exists(db_name):
        os.remove(db_name)
    db = sqlite3.connect(db_name)
    cursor = db.cursor()

    # create rat_runtimes
    cursor.execute(" CREATE TABLE rat_episodic_metrics "
                   " ( config        INTEGER, "
                   "   episode       INTEGER, "
                   "   rat           INTEGER, "
                   "   steps         REAL, "
                   "   error_rate    REAL, " # extra steps ratio
                   "   PRIMARY KEY ( config, episode, rat ) "
                   " ) "  # removed WITHOUT ROWID since sqlite version on circe does not support it
                   )

    cursor.execute(" CREATE TABLE rat_metrics "
                   " ( config        INTEGER, "
                   "   rat           INTEGER, "
                   "   seed          INTEGER, "
                   "   learning_time INTEGER, "
                   "   PRIMARY KEY ( config, rat ) "
                   " ) "  # removed WITHOUT ROWID since sqlite version on circe does not support it
                   )

    # create rat_summaries_steps and rat_summaries_error_rates
    summary_schema = """
                     CREATE TABLE {}
                     ( config   INTEGER,
                       episode  INTEGER,
                       count    INTEGER,
                       mean     REAL, 
                       std      REAL, 
                       min      REAL, 
                       [25%]    REAL, 
                       [50%]    REAL, 
                       [75%]    REAL, 
                       max      REAL, 
                       PRIMARY KEY ( config, episode )
                     )   
                     """  # removed WITHOUT ROWID since sqlite version on circe does not support it

    cursor.execute(summary_schema.format("rat_summaries_steps"))
    cursor.execute(summary_schema.format("rat_summaries_error_rate"))

    return db


def merge_and_store_rat_episodic_metics(config_folder, config_number, sample_rate, num_rats, num_episodes, db):
    """ Merges the episodic metrics (such as run times) of all rats in the config into a pandas data frame"""

    sample_episodes = np.arange(num_episodes, step=sample_rate, dtype=np.uint16)
    file_steps      = config_folder + "r{}-steps.bin"

    # create columns of the final data frame:
    metrics_df = pd.DataFrame({
        'config'  : config_number,
        'episode' : np.tile( sample_episodes, num_rats),
        'rat'     : np.repeat(np.arange(num_rats, dtype=np.uint8), len(sample_episodes)),
        'steps'   : np.concatenate([ load_int_vector(file_steps.format(r))[sample_episodes]  for r in range(num_rats)]) # this can be a very big number
    })


    # note: the shortest path is constant for one configuration of rats, since starting positions are predefined
    metrics_df['error_rate'] = (metrics_df.steps / load_int_vector(config_folder + "r0-shortest_path.bin")[0]) - 1

    metrics_df.to_sql('rat_episodic_metrics', db, if_exists='append', index=False)

    return metrics_df

def merge_and_store_rat_metrics(config_folder, config_number, num_rats, db):
    """ Merges the metrics of all rats (such as learning times) in the config into a pandas data frame"""

    seed_file = config_folder + "r{}-seed.bin"
    learning_time_file = config_folder + "r{}-learning_time.bin"

    # create columns of the final data frame:
    rat_metrics_df = pd.DataFrame({
        'config'        : config_number,
        'rat'           : np.arange(num_rats, dtype=np.uint8),
        'seed'          : [ load_long_vector(seed_file.format(r))[0] for r in range(num_rats)],
        'learning_time' : [ load_int_vector(learning_time_file.format(r))[0]  for r in range(num_rats)]
    })

    print(num_rats)
    print(config_number)
    print(np.arange(num_rats, dtype=np.uint8))
    print([ load_long_vector(seed_file.format(r))[0] for r in range(num_rats)])
    print([ load_int_vector(learning_time_file.format(r))[0]  for r in range(num_rats)])

    # save table
    rat_metrics_df.to_sql('rat_metrics', db, if_exists='append', index=False)

    # return the data frame
    return rat_metrics_df


def create_and_store_summaries(run_times, column, config_folder, db):
    # create a summary of the metric given by the column
    t = time.time()
    summaries = run_times.groupby(['config', 'episode'])[[column]].describe() # this takes the most amount of time: approx 1 min
    summaries.columns = summaries.columns.droplevel()
    summaries = summaries.reset_index()
    print('Time summarizing: {}'.format(time.time() - t))


    # set data types to reduce memory
    summaries['count']   = summaries['count'].astype(np.uint8) # we probably wont use more than 256 rats
    summaries.episode = summaries.episode.astype(np.uint16)    # we probably wont use more than 32k episodes
    for col in summaries.columns.drop(['count', 'episode']):   # all other columns should be float 32
        summaries[col] = summaries[col].astype(np.float32) 

    # save the summaries
    summaries.to_sql(f'rat_summaries_{column}', db, if_exists='append', index=False)


def process_config(base_folder, config, sample_rate):
    # tracemalloc.start()
    t1 = time.time()

    # get parameters
    base_folder   = os.path.join(base_folder, '')
    config_folder = os.path.join(base_folder, 'configs', config, '')
    config_number = np.uint16(config[1:])  # drop letter c and parse number
    num_rats      = len(glob.glob(config_folder + "r*-steps.bin"))
    print(config_folder)
    num_episodes  = read_vector_size(config_folder + "r0-steps.bin")

    # create database and tables to store results
    db = create_db_and_tables(config_folder)

    # merge results from all rats
    episodic_metrics = merge_and_store_rat_episodic_metics(config_folder, config_number, sample_rate, num_rats, num_episodes, db)
    rat_metrics      = merge_and_store_rat_metrics(config_folder, config_number, num_rats, db)

    create_and_store_summaries(episodic_metrics, 'steps', config_folder, db)
    create_and_store_summaries(episodic_metrics, 'error_rate', config_folder, db)

    print('TOTAL TIME: {}'.format(time.time() - t1))
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    # print('MEMORY: current {}MB, peak {}MB'.format(current / 10 ** 6, peak / 10 ** 6))



if __name__ == '__main__':
    # argv[1] = base folder
    # argv[2] = config
    # argv[3] = runtime sample rate
    runtime_sample_rate = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    process_config(sys.argv[1], sys.argv[2], runtime_sample_rate)


