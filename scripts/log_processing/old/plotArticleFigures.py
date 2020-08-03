import sys
from pythonUtils.VariableLoader import *
from plotnine import *
from pythonUtils.evaluation import *
import math
# from pandasgui import show

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
        ggsave(p, file_name + '-lim{:02d}.pdf'.format(int(lim)), dpi=100)

def plotStatisticalTest(df, column, config_renaming, title, savefile):
    dunnRes = dunn(df, ['config'], column)

    # reorder configs
    mapper = lambda x: int(x[1:])
    dunnRes = dunnRes.rename(mapper, axis=0).rename(mapper, axis=1)
    cols = dunnRes.columns.sort_values()
    dunnRes = dunnRes.loc[cols, cols]

    dunnRes = dunnRes.rename(config_renaming, axis=0).rename(config_renaming, axis=1)

    columnOrder = dunnRes.columns

    # melt for plotting
    dunnRes = dunnRes.reset_index().melt(id_vars='index', value_vars=dunnRes.columns)
    dunnRes['stat'] = dunnRes.value.map(statistic_to_color_mapper)

    # plot
    p = ggplot(dunnRes, aes('index', 'variable', fill='factor(stat)'))\
        + geom_tile(aes(width=.95, height=.95)) + ggtitle(title)\
        + scale_fill_manual(values=stat_colors) \
        + xlab('') + ylab('') \
        + scale_x_discrete(limits=columnOrder) \
        + scale_y_discrete(limits=columnOrder) \
        + theme(axis_text_x=element_text(rotation=45, hjust=1))
    ggsave(p, savefile, dpi=100)

############################################################################
##############            PLOT EXPERIMENTS                ##################
############################################################################

def plot_single_size_traces_experiment(base_folder, summaries_normalized, all_data, configs):

    location = 'gmean'

    # create plot folder
    article_folder = base_folder + 'articlePlots/'
    if not os.path.exists(article_folder):
        os.makedirs(article_folder)

    # append pcSizes and traces to data:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes', 'traces'])
    gmean_extended = data_extended.loc[data_extended.location == location, :]
    gmean_extended['Traces'] = gmean_extended.traces.map("{0:.2f}".format)

    # for each size, compare results of different traces, faceted on starting location
    for name, data in gmean_extended.groupby(['mazeFile', 'pcSizes']):
        maze = name[0].strip('.xml')
        size = "{0:.2f}".format(name[1])

        scale_folder = article_folder + 's{}/'.format(size)
        if not os.path.exists(scale_folder):
            os.makedirs(scale_folder)
        filename = scale_folder + 'optimality-VS-episode-{}'.format(maze)

        p0 = ggplot(data, aes('episode', '50%', color='Traces', group='Traces')) \
            + facet_wrap('location') \
            + ggtitle(maze + ' - scale ' + size) \
            + geom_line() \
            + xlab('Episode') + ylab('Median Optimality Ratio') \
            + theme(axis_text_x=element_text(rotation=45, hjust=1))
        zoom_and_save(p0, [0, 2.5, 5], filename)

    # DO BOX PLOTS OF LAST EPISODE

    # append pcSizes and traces, filter gmean
    all_data_extended = merge_config_data(all_data, configs, ['pcSizes', 'traces'])
    gmean_all_data = all_data_extended.loc[all_data_extended.location == location, :]
    last_episodes_gmean_data = gmean_all_data.loc[gmean_all_data.episode == gmean_all_data.episode.max(), :]
    last_episodes_gmean_data['Traces'] = last_episodes_gmean_data.traces.map("{0:.2f}".format)

    # boxplots of last episode of each scale

    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in last_episodes_gmean_data.groupby(['mazeFile', 'pcSizes']):
        maze = name[0].strip('.xml')
        size = "{0:.2f}".format(name[1])

        scale_folder = article_folder + 's{}/'.format(size)
        filename = scale_folder + 'boxPlotsLastEpisodes-{}'.format(maze)

        p0 = ggplot(data, aes('Traces', 'normalized'))\
             + geom_point(alpha=0.) \
             + geom_jitter(alpha=0.4) \
             + geom_boxplot(color='blue', alpha=0.0, notch=False, outlier_alpha=0) \
             + ggtitle('{} - L {}'.format(maze, location)) \
             + xlab("Scale") \
             + ylab("Optimality Ratio") \
             + theme(axis_text_x=element_text(rotation=45, hjust=1))
        zoom_and_save(p0, [0, 2.5, 5], filename)

        # do dunntest
        dunn_filename = scale_folder + 'dunnTest-{}.pdf'.format(maze)
        config_names = lambda x: "{0:.2f}".format(configs.loc['c{}'.format(x), 'traces'])
        plotStatisticalTest(data, 'normalized', config_names, maze, dunn_filename)


def plot_single_size(base_folder, summaries_normalized, all_data, configs):

    location = 'gmean'

    # create plot folder
    article_folder = base_folder + 'articlePlots/'
    if not os.path.exists(article_folder):
        os.makedirs(article_folder)

    # append pcSizes to data and filter:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes'])
    gmean_data = data_extended.loc[data_extended.location == location, :]
    gmean_data['Scale'] = gmean_data.pcSizes.astype(str)

    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in gmean_data.groupby(['mazeFile']):
        maze = name.strip('.xml')
        filename = article_folder + 'optimality-VS-episode-{}'.format(maze)

        p0 = ggplot(data, aes('episode', '50%', color='Scale', group='Scale'))\
            + geom_line()\
            + xlab('Episode') + ylab('Median Optimality Ratio')\
            + ggtitle('{} - L {}'.format(maze, location))\
            + theme(axis_text_x=element_text(rotation=45, hjust=1))

        zoom_and_save(p0, [0, 5, 2.5], filename)

    # DO BOX PLOTS OF LAST EPISODE

    # append pcSizes, filter gmean
    all_data_extended = merge_config_data(all_data, configs, ['pcSizes'])
    gmean_all_data = all_data_extended.loc[all_data_extended.location == location, :]
    last_episodes_gmean_data = gmean_all_data.loc[gmean_all_data.episode == gmean_all_data.episode.max(), :]

    # boxplots of last episode of each scale

    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in last_episodes_gmean_data.groupby(['mazeFile']):
        maze = name.strip('.xml')
        filename = article_folder + 'boxPlotsLastEpisodes-{}'.format(maze)

        print(data.columns)

        p0 = ggplot(data, aes('factor(pcSizes)', 'normalized'))
        p0 = p0 + geom_point(alpha=0.)\
            + geom_jitter(alpha=0.4)\
            + geom_boxplot(color='blue', alpha=0.0, notch=False, outlier_alpha=0)\
            + ggtitle('{} - L {}'.format(maze,location))\
            + xlab("Scale")\
            + ylab("Optimality Ratio")\
            + theme(axis_text_x=element_text(rotation=45, hjust=1))
        zoom_and_save(p0, [0, 2.5, 5], filename)

        # do dunntest
        dunn_filename = article_folder + 'dunnTest-{}.pdf'.format(maze)
        config_names = lambda x: str(configs.loc['c{}'.format(x), 'pcSizes'])
        plotStatisticalTest(data, 'normalized', config_names, maze, dunn_filename)


def plot_two_scales(base_folder, summaries_normalized, all_data, configs):

    location = 'gmean'

    # create plot folder
    article_folder = base_folder + 'articlePlots/'
    combinations_folder = article_folder + 'combinations/'
    if not os.path.exists(combinations_folder):
        os.makedirs(combinations_folder)

    # append pcSizes to data, filter then split scales:
    data_extended = merge_config_data(summaries_normalized, configs, ['pcSizes'])
    gmean_data = data_extended.loc[data_extended.location == location, :]
    split_column(gmean_data, 'pcSizes', ['s0', 's1'])
    gmean_data['Scales'] = gmean_data['pcSizes'].astype(str)

    # load data from the single size experiment:
    single_size_folder = os.path.dirname(os.path.normpath(base_folder)) + '/experiment5-single/'
    # single_size_folder = 'singleSizeTraces0Experiment/'
    # if base_folder == 'twoScalesWithTracesExperiment/':
    #     single_size_folder = 'singleSizeExperiment2/'
    single_configs = load_config_file(single_size_folder)
    single_data = load_summaries_normalized(single_size_folder)
    single_data_extended = merge_config_data(single_data, single_configs, ['pcSizes'])
    single_gmean_data = single_data_extended.loc[single_data_extended.location == location, :]
    single_gmean_data['s0'] = single_gmean_data['pcSizes'].astype(str)
    single_gmean_data['s1'] = single_gmean_data['pcSizes'].astype(str)
    single_gmean_data['Scales'] = single_gmean_data['pcSizes'].astype(str)


    # combine data from both experiments:
    cols = ['mazeFile', 'Scales', 's0', 's1', 'episode', '50%']
    combined_summaries = pd.concat([gmean_data[cols], single_gmean_data[cols]], ignore_index=True)


    # for each maze, scale, compare all combinations using that scale
    for name, data in combined_summaries.groupby(['mazeFile']):
        maze = name
        print('maze: ', maze)


        for scale in [0.04*i for i in range(1, 15)]:
            scale_str = str(scale)
            print('scale: {:0.2f}'.format(scale))


            scale_folder = article_folder + 's{:0.2f}/'.format(scale)
            if not os.path.exists(scale_folder):
                os.makedirs(scale_folder)

            filename = scale_folder + 'optimality-VS-episode-{}'.format(maze)

            scale_data = data.loc[(data.s0 == scale_str) | (data.s1 == scale_str), :].reset_index()
            scale_data['Second Scale'] = scale_str
            scale_data.loc[scale_data.s0 != scale_str, 'Second Scale'] = scale_data['s0'][scale_data.s0 != scale_str]
            scale_data.loc[scale_data.s1 != scale_str, 'Second Scale'] = scale_data['s1'][scale_data.s1 != scale_str]

            # size_mapping = {'{:0.2f}'.format(s): 0.1 for s in [0.04*i for i in range(1, 15)]}
            # size_mapping['{:0.2f}'.format(scale)] = 0.3
            size_mapping = [2.3 if s == scale else 1 for s in [0.04*i for i in range(1, 15)]]

            print(size_mapping)

            #
            p0 = ggplot(scale_data, aes('episode', '50%', color='Second Scale', group='Second Scale')) \
                + geom_line(aes(size='Second Scale')) \
                + scale_size_manual(values=size_mapping) \
                + xlab('Exlapisode') + ylab('Median Optimality Ratio') \
                + ggtitle('{} - Scale {:0.2f}'.format(maze, scale)) \
                + theme(axis_text_x=element_text(rotation=45, hjust=1))

            zoom_and_save(p0, [0, 2.5, 5], filename)

            # for each combination plot the combination
            for scale2 in [0.04 * i for i in range(1, 15)]:

                if scale != scale2:
                    combination_filename = combinations_folder + \
                                           '{}-s{}-s{}'.format(maze, round(scale*100), round(scale2*100))
                    pcSizes = ['{}'.format(scale),
                               '{}'.format(scale2),
                               '{},{}'.format(scale2, scale),
                               '{},{}'.format(scale, scale2)
                               ]

                    combination_data = data.loc[data.Scales.isin(pcSizes), :]

                    p2 = ggplot(combination_data, aes('episode', '50%', color='Scales', group='Scales')) \
                         + geom_line() \
                         + xlab('Episode') + ylab('Median Optimality Ratio') \
                         + ggtitle('{} - Scale {:0.2f}'.format(maze, scale)) \
                         + theme(axis_text_x=element_text(rotation=45, hjust=1))

                    zoom_and_save(p2, [0, 2.5, 5], combination_filename)


    # For each combination plot dunn test

    # load data from single size experiment
    all_data_single = load_runtimes(single_size_folder)

    # filter data
    last_episode_data = all_data.loc[all_data.episode == all_data.episode.max(), :]
    all_data_filtered = last_episode_data.loc[last_episode_data.location == location, :]
    all_extended = merge_config_data(all_data_filtered, configs, ['pcSizes'])

    last_episode_data_single = all_data_single.loc[all_data_single.episode == all_data_single.episode.max(), :]
    all_data_single_filtered = last_episode_data_single.loc[last_episode_data_single.location == location, :]
    all_single_extended = merge_config_data(all_data_single_filtered, single_configs, ['pcSizes'])
    all_single_extended['pcSizes'] = all_single_extended['pcSizes'].astype(str)


    # combine data
    cols_all_data = ['mazeFile', 'pcSizes', 'normalized']
    all_data_combined = pd.concat([all_extended[cols_all_data],
                                   all_single_extended[cols_all_data]],
                                   ignore_index=True)

    for name, data in all_data_combined.groupby(['mazeFile']):
        maze = name
        print('maze: ', maze)

        print('ALL: ', data.pcSizes.unique())

        for scale in [0.04 * i for i in range(1, 15)]:
            for scale2 in [0.04 * i for i in range(1, 15)]:
                if scale != scale2:

                    # get data and perform dunn test

                    pcSizes = ['{}'.format(scale),
                               '{}'.format(scale2),
                               '{},{}'.format(scale2, scale),
                               '{},{}'.format(scale, scale2)
                               ]
                    # print(data.pcSizes)
                    dunn_data = data.loc[data.pcSizes.isin(pcSizes), :]
                    dunn_data['config'] = 'c0'
                    dunn_data.loc[dunn_data.pcSizes == pcSizes[0], 'config'] = 'c1'
                    dunn_data.loc[dunn_data.pcSizes == pcSizes[1], 'config'] = 'c2'

                    dunn_filename = combinations_folder + \
                                    'dunnTest-{}-s{}-s{}.pdf'.format(maze, round(scale*100),round(scale2*100))
                    config_names = lambda x: pcSizes[(x+3)%4]
                    plot_title = '{} - {}'.format(maze,pcSizes[3])

                    # print(dunn_data.pcSizes.unique(), pcSizes)
                    plotStatisticalTest(dunn_data, 'normalized', config_names, plot_title, dunn_filename)


def plot_single_size_vs_mazes(base_folder, summaries_normalized, all_data, configs):
    # plot performance vs episode
    # one plot for each (maze,starting_location) pair
    # color = scale
    # no facets

    location  = '1'

    # create plot folder
    article_folder = base_folder + 'articlePlots/location1/'
    maze_plot_folder = article_folder + 'mazePlots/'
    scale_plot_folder = article_folder + 'scales/'
    if not os.path.exists(maze_plot_folder):
        os.makedirs(maze_plot_folder)
    if not os.path.exists(scale_plot_folder):
        os.makedirs(scale_plot_folder)


    # filter data then append pcSizes:
    gmean_data = summaries_normalized.loc[summaries_normalized.location == location, :]
    data_extended = merge_config_data(gmean_data, configs, ['pcSizes'])

    data_extended['Scale'] = data_extended.pcSizes.astype(str)


    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in data_extended.groupby(['mazeFile']):
        maze = name.strip('.xml')

        filename = maze_plot_folder + '{}-performance'.format(maze)

        p0 = ggplot(data, aes('episode', '50%', color='Scale', group='Scale'))\
            + geom_line() + xlab('Episode') + ylab('Optimality Ratio')\
            + ggtitle('{}'.format(maze))\
            + theme(axis_text_x=element_text(rotation=45, hjust=1))
        zoom_and_save(p0, [0, 2.5, 5], filename)


    # for each maze and location plot mean (or median) runtimes for each size
    for name, data in data_extended.groupby(['pcSizes']):
        scale = name

        filename = scale_plot_folder + 'S{:02d}-performance'.format(round(scale*100))

        p0 = ggplot(data, aes('episode', '50%', color='mazeFile', group='mazeFile')) \
             + geom_line() + xlab('Episode') + ylab('Optimality Ratio')\
             + ggtitle('Scale {}'.format(scale))

        zoom_and_save(p0, [0, 2.5, 5], filename)


    # do boxplots and dunn tests for each maze

    # append pcSizes, filter gmean
    all_data_extended = merge_config_data(all_data, configs, ['pcSizes'])
    gmean_all_data = all_data_extended.loc[all_data_extended.location == location, :]
    last_episodes_gmean_data = gmean_all_data.loc[gmean_all_data.episode == gmean_all_data.episode.max(), :]

    # boxplots of last episode of each scale

    # for each maze plot mean (or median) runtimes for each size
    for name, data in last_episodes_gmean_data.groupby(['mazeFile']):
        maze = name.strip('.xml')
        filename = maze_plot_folder + '{}-boxPlots'.format(maze)

        p0 = ggplot(data, aes('factor(pcSizes)', 'normalized'))
        p0 = p0 + geom_point(alpha=0.) \
             + geom_jitter(alpha=0.4) \
             + geom_boxplot(color='blue', alpha=0.0, notch=False, outlier_alpha=0) \
             + ggtitle('{}'.format(maze)) \
             + xlab("Scale") \
             + ylab("Optimality Ratio") \
             + theme(axis_text_x=element_text(rotation=45, hjust=1))
        zoom_and_save(p0, [0, 2.5, 5], filename)

        # do dunntest
        dunn_filename = maze_plot_folder + '{}-dunnTest.pdf'.format(maze)
        config_names = lambda x: str(configs.loc['c{}'.format(x), 'pcSizes'])
        plotStatisticalTest(data, 'normalized', config_names, maze, dunn_filename)

    # for each maze plot mean (or median) runtimes for each size
    for name, data in last_episodes_gmean_data.groupby(['pcSizes']):
        scale = name

        filename = scale_plot_folder + 'S{:02d}-boxPlots'.format(round(scale * 100))

        p0 = ggplot(data, aes('mazeFile', 'normalized'))
        p0 = p0 + geom_point(alpha=0.) \
             + geom_jitter(alpha=0.4) \
             + geom_boxplot(color='blue', alpha=0.0, notch=False, outlier_alpha=0) \
             + ggtitle('{}'.format(maze)) \
             + xlab("Scale") \
             + ylab("Optimality Ratio") \
             + theme(axis_text_x=element_text(rotation=45, hjust=1))
        zoom_and_save(p0, [0, 2.5, 5], filename)

        # do dunntest
        dunn_filename = scale_plot_folder + 'S{:02d}-dunnTest.pdf'.format(round(scale * 100))
        config_names = lambda x: str(configs.loc['c{}'.format(x), 'mazeFile'])
        plotStatisticalTest(data, 'normalized', config_names, '{}'.format(scale), dunn_filename)



def plot_memory_reduction_experiment(base_folder, summaries_normalized, all_data, configs):

    location ='gmean'

    # create plot folder
    article_folder = base_folder + 'articlePlots/'
    if not os.path.exists(article_folder):
        os.makedirs(article_folder)



    def totalPCs(numPCx):
        nx = numPCx.split(sep=',')
        nx0 = int(nx[0])
        n0 = nx0*math.floor(nx0*3/2.2)

        nx1 = int(nx[1]) if len(nx)>1 else 0
        n1 = nx1*math.floor(nx1*3/2.2)

        return n0 + n1

    # filter data then append numPCx:
    gmean_data = summaries_normalized.loc[summaries_normalized.location == location, :]
    data_extended = merge_config_data(gmean_data, configs, ['numPCx'])
    data_extended['Num_PCs'] = data_extended.numPCx.map(totalPCs)

    # format for saving file:
    filename = article_folder + 'optimality-VS-episode-M0'

    sizes = [0.5 for i in range(16)]
    sizes[-1] = 2.3

    p0 = ggplot(data_extended, aes('episode', '50%', color='factor(Num_PCs)', group='Num_PCs')) \
        + geom_line(aes(size='factor(Num_PCs)')) \
        + scale_size_manual(values=sizes) \
        + xlab('Episode') + ylab('Median Optimality Ratio') \
        + theme(axis_text_x=element_text(rotation=45, hjust=1)) \
        + ggtitle('Memory Reduction Experiment')

    zoom_and_save(p0, [0, 5, 2.5], filename)

    # DO BOX PLOTS OF LAST EPISODE

    # append numPCx, filter gmean
    last_data = all_data.loc[all_data.episode == all_data.episode.max(), :]
    gmean_all_data = last_data.loc[last_data.location == location, :]
    all_data_extended = merge_config_data(gmean_all_data, configs, ['numPCx'])
    all_data_extended['Num_PCs'] = all_data_extended.numPCx.map(totalPCs)

    # boxplots of last episode of each scale

    # plot box plots
    filename = article_folder + 'boxPlotsLastEpisodes'


    p0 = ggplot(all_data_extended, aes('factor(Num_PCs)', 'normalized'))\
         + geom_point(alpha=0.) \
         + geom_jitter(alpha=0.4) \
         + geom_boxplot(color='blue', alpha=0.0, notch=False, outlier_alpha=0) \
         + xlab("Scale") \
         + ylab("Optimality Ratio") \
         + theme(axis_text_x=element_text(rotation=45, hjust=1))
    zoom_and_save(p0, [0, 2.5, 5], filename)

    # do dunntest
    dunn_filename = article_folder + 'dunnTest.pdf'
    config_names = lambda x: str(totalPCs(configs.loc['c{}'.format(x), 'numPCx']))
    plotStatisticalTest(all_data_extended, 'normalized', config_names, '', dunn_filename)




def process_all_configs(folder):
    # load data
    # runtimes, summaries, summaries_normalized, configs = load_data(base_folder)
    print(folder)

    experiment_name = os.path.basename(os.path.normpath(folder))
    normalized_summaries = load_summaries_normalized(folder)
    all_data = load_runtimes(folder)
    configs_df = load_config_file(folder)

    if experiment_name == 'experiment1-traces':
        plot_single_size_traces_experiment(folder, normalized_summaries, all_data, configs_df)

    # if experiment_name == os.path.join('singleSizeExperiment', '') or \
    #         folder == os.path.join('singleSizeExperiment2', '') or \
    #         folder == os.path.join('singleSizeSameNumber', '') or \
    #         folder == os.path.join('singleSizeSameNumberMoreEpisodes', ''):
    if experiment_name == 'experiment2-singleMin' or \
            experiment_name == 'experiment3-singleSame':
        plot_single_size(folder, normalized_summaries, all_data, configs_df)

    if experiment_name == 'experiment4-mazes':
        plot_single_size_vs_mazes(folder, normalized_summaries, all_data, configs_df)

    if experiment_name == 'experiment5-twoScales':
        plot_two_scales(folder, normalized_summaries, all_data, configs_df)



    # if folder == os.path.join('memoryReductionExperiment', '') or \
    #         folder == os.path.join('memoryReductionExperiment2', ''):
    #     plot_memory_reduction_experiment(folder, normalized_summaries, all_data, configs_df)

    print('No matches')

if __name__ == '__main__':
    process_all_configs(os.path.join(sys.argv[1], ''))
