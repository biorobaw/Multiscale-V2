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
    cursor.execute(" CREATE TABLE rat_runtimes "
                   " ( config   INTEGER, "
                   "   location INTEGER, "
                   "   episode  INTEGER, "
                   "   rat      INTEGER, "
                   "   steps       REAL, "
                   "   errors      REAL, "
                   "   deltaV      REAL, "
                   "   PRIMARY KEY ( config, location, episode, rat ) "
                   " ) "  # removed WITHOUT ROWID since sqlite version on circe does not support it
                   )

    # create rat_summaries and rat_summaries_normalized
    summary_schema = """
                     CREATE TABLE {}
                     ( config   INTEGER,
                       location INTEGER,
                       episode  INTEGER,
                       count    INTEGER,
                       mean     REAL, 
                       std      REAL, 
                       min      REAL, 
                       [25%]    REAL, 
                       [50%]    REAL, 
                       [75%]    REAL, 
                       max      REAL, 
                       deltaV   REAL, 
                       PRIMARY KEY ( config, location, episode )
                     )   
                     """  # removed WITHOUT ROWID since sqlite version on circe does not support it

    cursor.execute(summary_schema.format("rat_summaries"))
    cursor.execute(summary_schema.format("rat_summaries_errors"))

    seed_table_schema = """
        CREATE TABLE rat_seeds
                     ( config   INTEGER,
                       rat      INTEGER,
                       seed     INTEGER, 
                       PRIMARY KEY ( config, rat )
                     )  
    """
    cursor.execute(seed_table_schema)

    return db



# def get_maze_metrics(base_folder, config, step_size):
def get_maze_metrics(base_folder, config):
    # find maze of the config
    configs = pd.read_csv(base_folder + 'configs.csv', sep='\t')
    configs = configs.drop(columns=['run_id']).drop_duplicates()
    configs = configs.set_index(['config'])
    config_maze = os.path.basename(configs.loc[config]['mazeFile'])

    # find maze metrics (calculate max error of all  locations per episode and add it to DF)
    maze_metrics = pd.read_csv(base_folder + "mazes/mazeMetrics.csv")
    maze_metrics = maze_metrics.set_index(['maze', 'pos']).loc[config_maze]
    return maze_metrics

def merge_runtimes_from_all_rats(config_folder, sample_rate):
    """ Merges the run times of all rats in the config into a pandas data frame"""
    # get number of rats and starting locations in this experiment:
    num_locations = np.unique(load_int_vector(config_folder + "r0-steps.bin")).size
    num_episodes  = read_vector_size(config_folder + "r0-steps.bin") // num_locations
    episode_ids = np.arange(num_episodes, step=sample_rate, dtype=np.uint16)
    num_samples_episodes = len(episode_ids)
    num_rats = len(glob.glob(config_folder + "r*-V0.bin"))

    # create columns of the final data frame:
    rat_ids = np.repeat(np.arange(num_rats, dtype=np.uint8), num_locations * num_samples_episodes)
    episode = np.tile(np.repeat(episode_ids, num_locations), num_rats)
    locations = np.zeros(num_samples_episodes * num_locations * num_rats, dtype=np.uint8)
    steps  = np.zeros(num_samples_episodes * num_locations * num_rats, dtype=np.float32)
    deltaV = np.zeros(num_samples_episodes * num_locations * num_rats, dtype=np.float32)

    # load info of each rat
    append_length = num_samples_episodes * num_locations
    sample_ids = np.arange(num_episodes * num_locations) \
        .reshape(-1, num_locations)[episode_ids] \
        .reshape(-1)
    file_name = config_folder + "r{}-steps.bin"
    deltaV_file_name = config_folder + "r{}-deltaV.bin"
    for rat_id in range(0, num_rats):
        r_start = append_length * rat_id
        r_end   = r_start+append_length
        with open(file_name.format(rat_id), 'rb') as file:
            locations[r_start:r_end] = load_int_vector(file)[sample_ids]
            steps[r_start:r_end] = load_int_vector(file)[sample_ids]

        deltaV[r_start:r_end] = load_float_vector(deltaV_file_name.format(rat_id))[sample_ids]

    # create data frame from the columns
    return pd.DataFrame({'location': locations,
                         'episode': episode,
                         'rat': rat_ids,
                         'steps': steps,
                         'deltaV': deltaV
                         })


def merge_seeds_from_all_rats(config_folder, config_number):
    num_rats = len(glob.glob(config_folder + "r*-V0.bin"))
    rats  = np.arange(num_rats, dtype=np.uint8)
    seeds = np.zeros(num_rats, dtype=np.int64)
    file_name = config_folder + "r{}-seed.bin"
    for rat_id in range(0, num_rats):
        with open(file_name.format(rat_id), 'rb') as file:
            seeds[rat_id] = load_long_vector(file)[0]
    return pd.DataFrame({
        'config' : config_number,
        'rat'    : rats,
        'seed'   : seeds
    })


def process_and_save_location_runtimes(run_times, location, config_folder, config_number, db):
    # save run times
    run_times = run_times.copy()
    run_times.to_sql('rat_runtimes', db, if_exists='append', index=False)


    # create a summary

    # summarize run times
    t = time.time()
    summary_steps = run_times[['episode', 'steps']] \
        .groupby(['episode']) \
        .describe() # this takes the most amount of time: approx 1 min
    summary_steps.columns = summary_steps.columns.droplevel()

    summary_errors = run_times[['episode', 'errors']] \
        .groupby(['episode']) \
        .describe() # this takes the most amount of time: approx 1 min
    summary_errors.columns = summary_errors.columns.droplevel()


    # summarize deltaV and add it to summary
    dV = run_times[['episode', 'deltaV']] \
        .groupby(['episode'])\
        .mean()
    summary_steps = summary_steps.join(dV)
    summary_errors = summary_errors.join(dV)


    print('Summarizing: {}'.format(time.time() - t))
    summary_steps = summary_steps.reset_index()
    summary_errors = summary_errors.reset_index()


    # set data types to reduce memory
    for summary in [summary_steps, summary_errors]:
        summary['count']   = summary['count'].astype(np.uint8)
        summary.episode = summary.episode.astype(np.uint16)
        for col in summary.columns.drop(['count', 'episode']):
            # m_type = np.float32 if col not in ['mean', 'std'] and location != -1 else np.float32
            summary[col] = summary[col].astype(np.float32)

        # add location and config to dataframe
        summary.insert(loc=0, column='location', value=location)
        summary.insert(loc=0, column='config', value=config_number)


    # save the summary
    summary_steps.to_sql('rat_summaries', db, if_exists='append', index=False)
    summary_errors.to_sql('rat_summaries_errors', db, if_exists='append', index=False)


def process_config(base_folder, config, sample_rate):
    # tracemalloc.start()
    t1 = time.time()

    # get parameters
    base_folder = os.path.join(base_folder, '')
    config_folder = os.path.join(base_folder, 'configs', config, '')
    config_number = np.uint16(config[1:])  # drop letter c and parse number

    # get maze metrics:
    maze_metrics = get_maze_metrics(base_folder, config)

    # merge results from all rats
    all_run_times = merge_runtimes_from_all_rats(config_folder, sample_rate)
    all_run_times.insert(loc=0, column='config', value=config_number)
    all_run_times['errors'] = (all_run_times.steps / all_run_times.location.map(dict(maze_metrics.steps)) - 1).astype(np.float32)
    all_seeds = merge_seeds_from_all_rats(config_folder, config_number)


    # create database and tables to store results
    db = create_db_and_tables(config_folder)

    # store seeds in database
    all_seeds.to_sql('rat_seeds', db, if_exists='append', index=False)


    # divide results according to location and process them
    for location, run_times in all_run_times.groupby('location'):
        print('Processing location {}...'.format(location))
        process_and_save_location_runtimes(run_times, np.uint8(location), config_folder, config_number, db)
        print()

    # aggregate rat run_times by location
    print('aggregating rats...')
    mean_run_times = all_run_times.groupby(['episode', 'rat'])['steps', 'errors', 'deltaV'] \
        .mean() \
        .reset_index()
    mean_run_times.steps = mean_run_times.steps.astype(np.float32)
    mean_run_times.errors = mean_run_times.errors.astype(np.float32)
    mean_run_times.deltaV = mean_run_times.deltaV.astype(np.float32)


    location = np.uint8(-1)
    mean_run_times['location'] = location
    mean_run_times['config'] = config_number
    # add back location and


    # process aggregated results
    print('processing aggregated results...')
    process_and_save_location_runtimes(mean_run_times, np.uint8(location), config_folder, config_number, db)

    print('TOTAL TIME: {}'.format(time.time() - t1))
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    # print('MEMORY: current {}MB, peak {}MB'.format(current / 10 ** 6, peak / 10 ** 6))

    # old code that might be usefule in the future:
    # config_geom_means = rat_geom_means.groupby(['episode'])['geom_mean'].agg({'geom_mean': ['mean', 'std']})
    # config_geom_means = config_geom_means.rename(columns={'mean': 'avg_geom_mean', 'std': 'std_geom_mean'})
    # config_geom_means = config_geom_means.reset_index()






# def process_all_configs(base_folder):
#     config_folders = get_list_of_configs(base_folder)
#     # config_folders = ['c'+str(i) for i in range(266, 280)]
#     for config in config_folders:
#         print("processing: ", config)
#         process_config(base_folder, config)


if __name__ == '__main__':
    # argv[1] = base folder
    # argv[2] = config
    # argv[3] = runtime sample rate
    runtime_sample_rate = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    process_config(sys.argv[1], sys.argv[2], runtime_sample_rate)


