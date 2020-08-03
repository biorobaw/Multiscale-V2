import sys
from pythonUtils.VariableLoader import *
from plotnine import *

"""
   This file is to be called after processAllConfigs,
   it creates the plots for the multi_scale_memory model 
   that require information from multiple configurations   
"""


def load_runtimes(folder):
    runtimes = pd.read_pickle(folder + 'runtimes.pickle')
    rename_location(runtimes)
    return runtimes


def load_summaries(folder):
    summaries = pd.read_pickle(folder + 'summaries.pickle')
    rename_location(summaries)
    return summaries


def load_summaries_normalized(folder):
    summaries_normalized = pd.read_pickle(folder + 'summaries_normalized.pickle')
    rename_location(summaries_normalized)
    return summaries_normalized


def rename_location(df):
    df.loc[df.location == -1, 'location'] = 'gmean'
    df['location'] = df.location.astype(str)


def split_column(df, column, new_titles):
    df[new_titles] = df[column].str.split(',', expand=True)


def merge_config_data(df1, configs, config_columns):
    return df1.merge(configs[config_columns], on='config')


def zoom_and_save(plot, ylims, file_name):
    for lim in ylims:
        p = plot
        if lim != 0:
            p = p + coord_cartesian(ylim=(1, lim))
        ggsave(p, file_name + '-lim{:02d}.png'.format(int(lim)), dpi=100)


def plot_single_size(base_folder, summaries_normalized, configs):
    # plot performance vs episode
    # one plot for each (maze,starting_location) pair
    # color = scale
    # no facets

    # append pcSizes to data:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes'])

    # format for saving file:
    file_name_format = base_folder + 'plots/result-performanceVsEpisode-{}-L{}'

    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in data_extended.groupby(['mazeFile', 'location']):
        maze = name[0]
        location = name[1]
        filename = file_name_format.format(maze, location)

        p0 = ggplot(data, aes('episode', '50%', color='factor(pcSizes)', group='pcSizes'))
        p0 = p0 + geom_line()
        p0 = p0 + ggtitle('{} - Location {}'.format(maze, location))

        zoom_and_save(p0, [0, 5], filename)


def plot_memory_reduction_experiment(base_folder, summaries_normalized, configs):
    # plot performance vs episode
    # one plot for each (maze,starting_location) pair
    # color = scale
    # no facets

    # append pcSizes to data:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes', 'numPCx'])

    # format for saving file:
    filename = base_folder + 'plots/result-performanceVsEpisode'

    p0 = ggplot(data_extended, aes('episode', '50%', color='factor(numPCx)', group='numPCx')) \
        + geom_line() \
        + facet_wrap('location') \
        + ggtitle('Memory Reduction Experiment')

    zoom_and_save(p0, [0, 5, 2.5], filename)


def plot_single_size_vs_mazes(base_folder, summaries_normalized, configs):
    # plot performance vs episode
    # one plot for each (maze,starting_location) pair
    # color = scale
    # no facets

    # append pcSizes to data:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes'])

    # create folder to store per maze plots:
    maze_plot_folder = base_folder + 'plots/mazePlots/'
    if not os.path.exists(maze_plot_folder):
        os.makedirs(maze_plot_folder)

    # format for saving file:
    file_name_format = maze_plot_folder + '{}-performance'

    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in data_extended.groupby(['mazeFile']):
        maze = name

        filename = file_name_format.format(maze)

        p0 = ggplot(data, aes('episode', '50%', color='factor(pcSizes)', group='pcSizes'))\
            + facet_wrap('location') \
            + geom_line()\
            + ggtitle('{} - Performance per scale'.format(maze))

        zoom_and_save(p0, [0, 5], filename)

    # create plot of performance vs maze for each scale
    scale_plot_folder = base_folder + 'plots/scalePlots/'
    if not os.path.exists(scale_plot_folder):
        os.makedirs(scale_plot_folder)

    # format for saving file:
    file_name_format = scale_plot_folder + 'S{:0.2f}-performance'

    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in data_extended.groupby(['pcSizes']):
        scale = name

        filename = file_name_format.format(scale)

        p0 = ggplot(data, aes('episode', '50%', color='factor(mazeFile)', group='mazeFile')) \
            + facet_wrap('location') \
            + geom_line() \
            + ggtitle('Scale {} - Performance per maze'.format(scale))

        zoom_and_save(p0, [0, 5], filename)


def plot_single_size_traces_experiment(base_folder, summaries_normalized, configs):
    # one plot for each maze
    # color = trace value
    # facet = start location

    # append pcSizes and traces to data:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes', 'traces'])

    # format for saving file:
    file_name_format = base_folder + 'plots/result-performanceVsEpisode-{}-S{}'

    # for each size, compare results of different traces, faceted on starting location
    for name, data in data_extended.groupby(['mazeFile', 'pcSizes']):
        maze = name[0]
        size = "{0:.2f}".format(name[1])
        filename = file_name_format.format(maze, size)

        p0 = ggplot(data, aes('episode', '50%', color='factor(traces)', group='traces')) \
            + facet_wrap('location') \
            + ggtitle(maze + ' - scale ' + size) \
            + geom_line()

        zoom_and_save(p0, [0, 2.5, 5], filename)




def plot_two_scales(base_folder, summaries_normalized, configs):
    # plot 1:
        # one plot for each scale1
        # color = scale2
        # facet = location

    # extend data
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes'])

    # split both scales
    split_column(data_extended, 'pcSizes', ['s0', 's1'])

    # file name format
    file_name_fomat = base_folder + 'plots/result-performanceVsEpisode-{}-S{:0.2f}'

    # for each size, compare results of different traces, faceted on starting location
    for name, data in data_extended.groupby(['mazeFile']):
        maze = name
        print('maze: ', maze)

        for scale in [0.04*i for i in range(1, 15)]:
            scale_str = str(scale)
            print('scale: {:0.2f}'.format(scale))

            scale_data = data.loc[(data.s0 == scale_str) | (data.s1 == scale_str), :].reset_index()
            scale_data['second_scale'] = ''
            scale_data.loc[scale_data.s0 != scale_str, 'second_scale'] = scale_data['s0'][scale_data.s0 != scale_str]
            scale_data.loc[scale_data.s1 != scale_str, 'second_scale'] = scale_data['s1'][scale_data.s1 != scale_str]

            p0 = ggplot(scale_data, aes('episode', '50%', color='factor(second_scale)', group='second_scale')) \
                + facet_wrap('location') \
                + ggtitle('{} - Scale {:0.2f}'.format(maze, scale)) \
                + geom_line()

            zoom_and_save(p0, [0, 2.5, 5], file_name_fomat.format(maze, scale))

    # load data from the single size experiment:
    cols = ['location', 'episode', '50%', 'pcSizes']
    original_folder = 'singleSizeTraces0Experiment/'
    if base_folder == 'twoScalesWithTracesExperiment/':
        original_folder = 'singleSizeExperiment2/'
    single_configs = load_config_file(original_folder)
    single_data = load_summaries_normalized(original_folder)
    single_data = merge_config_data(single_data, single_configs, ['pcSizes']).set_index('mazeFile')[cols]

    # for each (s1,s2) plot performance vs episode for s1, s1 and (s1,s2)
    file_name_fomat = base_folder + 'plots/result-singleVsCombined-{}-S{}'
    for name, data in data_extended.groupby(['mazeFile', 'pcSizes']):
        maze = name[0]
        scales = name[1]
        scale_values = name[1].split(sep=',')

        maze_data = single_data.loc[maze]
        data_s01 = maze_data.loc[maze_data.pcSizes.isin(scale_values), :]

        full_data = pd.concat([data[cols], data_s01], ignore_index=True)

        p0 = ggplot(full_data, aes('episode', '50%', color='factor(pcSizes)', group='pcSizes')) \
            + facet_wrap('location') \
            + ggtitle('{} - Scales {}'.format(maze, scales)) \
            + geom_line()

        zoom_and_save(p0, [0, 2.5, 5], file_name_fomat.format(maze, scales))



def process_all_configs(folder):
    # load data
    # runtimes, summaries, summaries_normalized, configs = load_data(base_folder)
    print(folder)

    normalized_summaries = load_summaries_normalized(folder)
    configs_df = load_config_file(folder)

    if folder == os.path.join('singleSizeExperiment', '') or \
            folder == os.path.join('singleSizeExperiment2', '') or \
            folder == os.path.join('singleSizeSameNumber', '') or \
            folder == os.path.join('singleSizeSameNumberMoreEpisodes', ''):
        plot_single_size(folder, normalized_summaries, configs_df)

    if folder == os.path.join('singleSizeTracesExperiment', ''):
        plot_single_size_traces_experiment(folder, normalized_summaries, configs_df)

    if folder == os.path.join('twoScalesWithTracesExperiment', '') or \
            folder == os.path.join('twoScalesNoTracesExperiment', ''):
        plot_two_scales(folder, normalized_summaries, configs_df)

    if folder == os.path.join('singleSizeVsMazes', ''):
        plot_single_size_vs_mazes(folder, normalized_summaries, configs_df)

    if folder == os.path.join('memoryReductionExperiment', ''):
        plot_memory_reduction_experiment(folder, normalized_summaries, configs_df)

    print('No matches')

if __name__ == '__main__':
    process_all_configs(os.path.join(sys.argv[1], ''))
