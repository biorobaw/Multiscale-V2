import glob
import sys
import numpy as np
from scipy import stats
from pythonUtils.BinaryFiles import *
from pythonUtils.VariableLoader import *
import time
import sqlite3
from sqlite3 import Error






def get_maze_metrics(base_folder, config, step_size):
    # find maze of the config
    configs = pd.read_csv(base_folder + 'configs.csv', sep='\t')
    configs = configs.drop(columns=['run_id']).drop_duplicates()
    configs = configs.set_index(['config'])
    config_maze = os.path.basename(configs.loc[config]['mazeFile'])

    # find maze metrics (calculate geometric mean and add it to DF)
    maze_metrics = pd.read_csv(base_folder + "mazes/mazeMetrics.csv")
    metric_gmean = maze_metrics.groupby('maze')['distance'].apply(stats.gmean).reset_index(name='distance')
    metric_gmean['pos'] = -1
    maze_metrics = maze_metrics.append(metric_gmean, ignore_index=True, sort=True)
    maze_metrics = maze_metrics.set_index(['maze', 'pos']).loc[config_maze]
    maze_metrics['minSteps'] = maze_metrics['distance'] / step_size
    return maze_metrics

def merge_runtimes_from_all_rats(config_folder):
    """ Merges the run times of all rats in the config into a pandas data frame"""

    # get number of rats and starting locations in this experiment:
    num_locations = np.unique(load_int_vector(config_folder + "r0-steps.bin")).size
    num_episodes = read_vector_size(config_folder + "r0-steps.bin") // num_locations
    num_rats = len(glob.glob(config_folder + "r*-V0.bin"))

    # create columns of the final data frame:
    rat_ids = np.repeat(np.arange(num_rats, dtype=np.uint8), num_locations * num_episodes)
    episode = np.tile(np.repeat(np.arange(num_episodes, dtype=np.uint16), num_locations), num_rats)
    locations = np.zeros(num_episodes * num_locations * num_rats, dtype=np.uint8)
    steps = np.zeros(num_episodes * num_locations * num_rats, dtype=np.float32)

    # load info of each rat
    append_length = num_episodes * num_locations
    file_name = config_folder + "r{}-steps.bin"
    for rat_id in range(0, num_rats):
        r_start = append_length * rat_id
        r_end = append_length * (rat_id + 1)
        with open(file_name.format(rat_id), 'rb') as file:
            locations[r_start:r_end] = load_int_vector(file)
            steps[r_start:r_end] = load_int_vector(file)

    # create data frame from the columns
    return pd.DataFrame({'location': locations,
                         'episode': episode,
                         'rat': rat_ids,
                         'steps': steps
                         })

def process_and_save_runtimes(run_times, location, normalizer, config_folder, config_number, db):
    # save run times
    #run_times_file_name = 'run_times_l{}.pickle'.format(location)
    #run_times.to_pickle(config_folder + run_times_file_name)
    run_times = run_times.copy()
    run_times['normalized'] = run_times['steps'] / normalizer
    run_times.to_sql('rat_runtimes', db, if_exists='append', index=False)


    # create a summary

    t = time.time()
    summary = run_times[['episode', 'steps']] \
        .groupby(['episode']) \
        .describe() # this takes the most amount of time: approx 1 min
    print('Summarizing: {}'.format(time.time() - t))
    summary.columns = summary.columns.droplevel()
    summary = summary.reset_index()
    # set data types to reduce memory
    summary['count']   = summary['count'].astype(np.uint8)
    summary.episode = summary.episode.astype(np.uint16)
    for col in summary.columns.drop(['count', 'episode']):
        m_type = np.float32 if col not in ['mean', 'std'] and location != -1 else np.float32
        summary[col] = summary[col].astype(m_type)

    # add location and config to dataframe
    summary.insert(loc=0, column='location', value=location)
    summary.insert(loc=0, column='config', value=config_number)


    # save the summary
    summary.to_sql('rat_summaries', db, if_exists='append', index=False)

    # normalize and store nomalized results
    for col in ['mean', 'std', 'min', '25%', '50%', '75%', 'max']:
        summary[col] = (summary[col] / normalizer).astype(np.float32)

    summary.to_sql('rat_summaries_normalized', db, if_exists='append', index=False)


def process_config(base_folder, config):
    # tracemalloc.start()
    t1 = time.time()

    # get parameters
    base_folder = os.path.join(base_folder, '')
    config_folder = base_folder + config + '/'
    config_number = np.uint8(config[1:])  # drop letter c and parse number
    step_size = np.float32(0.08)

    # get maze metrics:
    maze_metrics = get_maze_metrics(base_folder, config, step_size)

    # merge results from all rats
    all_run_times = merge_runtimes_from_all_rats(config_folder)
    all_run_times.insert(loc=0, column='config', value=config_number)
    all_run_times['normalized'] = np.float32(0)


    # create database to store results (delete if it already exists)
    db_name = config_folder + 'config_results.sqlite'
    if os.path.exists(db_name):
        os.remove(db_name)
    db = sqlite3.connect(db_name)


    # divide results according to location and process them
    for location, run_times in all_run_times.groupby('location'):
        print('Processing location {}...'.format(location))
        normalizer = np.float32(maze_metrics['minSteps'].iloc[location])
        process_and_save_runtimes(run_times, np.uint8(location), normalizer, config_folder, config_number, db)
        print()

    # aggregate rat run_times by location
    print('aggregating rats...')
    mean_run_times = all_run_times.groupby(['episode', 'rat'])['steps'] \
        .apply(stats.gmean) \
        .reset_index(name='steps')
    mean_run_times.steps = mean_run_times.steps.astype(np.float32)
    normalizer = np.float32(maze_metrics['minSteps'].iloc[-1])
    location = np.uint8(-1)
    mean_run_times['location'] = location
    mean_run_times['config'] = config_number
    # add back location and

    # process aggregated results
    print('processing aggregated results...')
    process_and_save_runtimes(mean_run_times, np.uint8(location), normalizer, config_folder, config_number, db)

    print('TOTAL TIME: {}'.format(time.time() - t1))
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    # print('MEMORY: current {}MB, peak {}MB'.format(current / 10 ** 6, peak / 10 ** 6))

    # old code that might be usefule in the future:
    # config_geom_means = rat_geom_means.groupby(['episode'])['geom_mean'].agg({'geom_mean': ['mean', 'std']})
    # config_geom_means = config_geom_means.rename(columns={'mean': 'avg_geom_mean', 'std': 'std_geom_mean'})
    # config_geom_means = config_geom_means.reset_index()






def process_all_configs(base_folder):
    config_folders = get_list_of_configs(base_folder)
    # config_folders = ['c'+str(i) for i in range(266, 280)]
    for config in config_folders:
        print("processing: ", config)
        process_config(base_folder, config)

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' ocurred")

    return connection

if __name__ == '__main__':
    # argv[1] = base folder
    # argv[2] = config
    if len(sys.argv) > 2:
        process_config(sys.argv[1], sys.argv[2])
    else:
        process_all_configs(sys.argv[1])


