from pythonUtils.VariableLoader import *

"""
    File used to processes all configurations after each individual config has been processed.
    Used in multi_scale_memory experiment
    The file computes and stores the following:
        'calibrationAllResults.csv'
            csv = config . 'mean' . 'std' . 'median' . 'pcSizes', 'traces'
        'calibrationResults.csv' 
            csv = pcSizes . config  . traces
            config indicates config (trace) for which the performance was maximized for the given pcSize
        'ratGeomMeansExtended.pickle'
            df = 'rat' . 'episode' . 'geom_mean' . 'config' . 'traces'
"""


def load_config_geom_means(base_folder, config_name):
    return load_config_variable('configGeomMeans.pickle', base_folder, config_name)


def load_rat_geom_means(base_folder, config_name):
    return load_config_variable('ratGeomMeans.pickle', base_folder, config_name)


if __name__ == '__main__':

    # set trace base folder:
    traces_base_folder = 'singleSizeExperiment/calib/'

    # load config data
    configs = load_config_file(traces_base_folder)[['pcSizes', 'traces']].drop_duplicates()
    # configs = config -> pcSizes . traces
    config_names = get_list_of_configs(traces_base_folder)
    # config_names = ['c'+str(i) for i in range(0,20)]

    # load configuration results
    # 'df configGeomMeans' == config . episode . steps . avg_geom_mean . std_geom_mean
    # configGeomMeans = load_config_geom_means(traces_base_folder, config_names)
    ratGeomMeans = load_rat_geom_means(traces_base_folder, config_names)
    # df ratGeomMeans = config . rat . episode . geom_mean

    # calculate metrics of last 10 episodes to determine best trace for each cell size
    lastRatGeomMeans = ratGeomMeans[ratGeomMeans['episode'] >= 90]\
        .groupby(['config'])\
        .agg({'geom_mean': ['mean', 'std', 'median']})
    lastRatGeomMeans.columns = lastRatGeomMeans.columns.droplevel()
    # df lastRatGeomMeans = config . 'mean' . 'std' . 'median'

    # concat result with configs just for visualization:
    resultTable = lastRatGeomMeans.merge(configs, on='config').reset_index()\
        .set_index(['pcSizes', 'traces']).sort_index()
    # df resultTable = config . 'mean' . 'std' . 'median' . 'pcSizes', 'traces'

    # store results
    resultTable.to_csv(traces_base_folder + 'calibrationAllResults.csv', float_format='%.2f')

    # merge results with parameters:
    calibrationResults = lastRatGeomMeans.merge(configs, on='config')\
        .groupby(['pcSizes'])['mean']\
        .idxmin()\
        .reset_index(name='config')\
        .merge(configs['traces'], on='config')
    # calibrationResults = config . traces

    print(calibrationResults)

    # store results
    calibrationResults.set_index('pcSizes')\
        .to_csv(traces_base_folder+'calibrationResults.csv', index=False, float_format='%.2f')

    # get scales:
    ratGeomMeansExtended = ratGeomMeans.merge(configs, on='config').set_index('pcSizes')
    # ratGeomMeansExtended = 'pcSizes' -> 'rat', 'episode', 'geom_mean', 'config', 'traces'
    ratGeomMeansExtended.to_pickle(traces_base_folder + 'ratGeomMeansExtended.pickle')
