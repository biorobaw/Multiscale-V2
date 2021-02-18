import scikit_posthocs as sp
from plotnine import *
import os
import numpy as np
from .data_loader import *
from .pythonUtils.BinaryFiles import *
from ..utils.MazeParser import parse_maze

"""
   This file is to be called after processAllConfigs,
   it creates the plots for the multi_scale_memory model
   that require information from multiple configurations
"""


def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def zoom_and_save(plot, ylims, file_name):
    """
    Plots the same plot multiple time with different max y limits (different scales)
    :param plot: a plot to be plotted
    :param ylims: array of max y limits (0 means use full scale)
    :param file_name: name format fo the generate files
    :return:
    """
    for lim in ylims:
        p = plot
        if lim != 0:
            p = p + coord_cartesian(ylim=(1, lim))
        ggsave(p, file_name + '-lim{}.pdf'.format(lim), dpi=300)


def plot_time_series(data, x_column, y_column, 
                     group_labels, x_title, y_title, legend_title, plot_title, 
                     save_name, zoom_levels= [0, 2.5, 5], x_lims=[[0, 1000]]):
    p0 = ggplot(data, aes(x_column, y_column, color='factor(config)', group='config')) \
         + geom_line() \
         + labs(x=x_title, y=y_title, title=plot_title, caption='smt') \
         + scale_color_discrete(name=legend_title, labels=group_labels)
    zoom_and_save(p0, zoom_levels, save_name)
    for lim in x_lims:
        zoom_and_save(p0 + xlim(lim[0], lim[1]), zoom_levels, save_name + f'x{lim[0]}_{lim[1]}')



def plot_box_plot(data, y_column, group_labels, x_title, y_title, plot_title, save_name, zoom_levels=[0, 2.5, 5]):
    """
    Generate and save a boxplot from a dataframe.
    The plot is saved multiple times with different y limits according to zoom_levels.
    The dataframe must have an integer column 'config' representing the different groups.
    :param data: dataframe containing the data
    :param y_column: column representing the random variable
    :param group_labels: array containing the group names (must be sorted according to config number)
    :param x_title: title for the x axis
    :param y_title: title for the y axis
    :param plot_title: title for the plot
    :param save_name:  file name format for the plot
    :param zoom_levels: array of y limits (0 means full scale)
    :return:
    """
    p0 = ggplot(data, aes('factor(config)', y_column)) \
         + geom_point(alpha=0.) + geom_jitter(alpha=0.4) \
         + geom_boxplot(color='blue', alpha=0.0, notch=False, outlier_alpha=0) \
         + labs(x=x_title, y=y_title, title=plot_title) \
         + scale_x_discrete(labels=group_labels)\
         + theme(axis_text_x=element_text(rotation=45, hjust=0.5))
    zoom_and_save(p0, zoom_levels, save_name)


stat_colors = {'≥0.07': '#ef3b2c',
               '<0.07': '#a1d99b',
               '<0.05': '#238b45',
               '<0.03': '#005a32'
               }

def stat_range_values(stat):
    i = 0 if stat < 0    else \
        3 if stat < 0.03 else \
        2 if stat < 0.05 else \
        1 if stat < 0.07 else \
        0
    return [*stat_colors][i]





def plot_statistical_test(df, column, group_names, title, savefile):
    """
    Performs a dunn test,  plots and saves results
    :param df: the dataframe with the results, we assume the existence of column 'config'
    :param column: column in the dataframe representing the random variable to be tested
    :param group_names: map or function mapping configs to strings (group names), can be a pd.DataSeries
    :param title: title for the plot
    :param savefile: pdf or png file to save the results to
    :return:
    """
    dunnRes = sp.posthoc_dunn(df, group_col='config', val_col=column, p_adjust='holm')

    # reorder configs
    # dunnRes = dunnRes.loc[cols, cols] # cols must be a permutation of the group names
    dunnRes = dunnRes.rename(group_names, axis=0).rename(group_names, axis=1)

    columnOrder = dunnRes.columns

    # melt for plotting
    dunnRes = dunnRes.reset_index().melt(id_vars='index', value_vars=dunnRes.columns)
    dunnRes['stat'] = dunnRes.value.map(stat_range_values)

    # plot
    p = ggplot(dunnRes, aes('index', 'variable', fill='factor(stat)'))\
        + geom_tile(aes(width=.95, height=.95)) + ggtitle(title)\
        + scale_fill_manual(values=stat_colors, name='p value') \
        + scale_x_discrete(limits=columnOrder) \
        + scale_y_discrete(limits=columnOrder) \
        + labs(x='', y='', title=title) \
        + theme(axis_text_x=element_text(rotation=45, hjust=1))
    ggsave(p, savefile, dpi=300)


def plot_runtimes_boxplots_dunntest(db, configs, location, episode, group_name,
                                    legend_title, legend_values,  plot_title, save_folder, 
                                    skip_runtimes=False, skip_boxplots=False, skip_dunntest=False,
                                    xlims = [[0,1000]]):

    # get config  indices and then get data from db
    indices = [np.uint16(c[1:]) for c in configs.index]  # config numbers
    if not skip_runtimes:
        summaries = load_summaries(db, indices, location)
    if not skip_boxplots or not skip_dunntest:
        runtimes_last_episode = load_episode_runtimes(db, indices, location, episode)

    # print("configs: ", pd.unique(runtimes_last_episode.config))

    # print(runtimes_last_episode.groupby(['config'])['location'].describe())
    # print(runtimes_last_episode.groupby(['config'])['episode'].describe())
    # print(runtimes_last_episode.groupby(['config'])['steps'].describe())

    # prepare save folder
    save_folder = os.path.join(save_folder , group_name, '')
    make_folder(save_folder)
    suffix = '' if group_name == '' else f'_{group_name}'

    # do the actual plotting
    if not skip_runtimes:
        plot_time_series(summaries, 'episode', 'steps', legend_values,
                         'episode', 'optimality ratio', legend_title, plot_title,
                         save_folder + f'runtimes{suffix}', [0, 1.3, 1.8], x_lims = xlims
                         )

    if not skip_boxplots:
        plot_box_plot(runtimes_last_episode, 'steps', legend_values,
                      'trace', 'optimality ratio', plot_title,
                      save_folder + f'boxplot{suffix}', [0, 1.3, 1.8])

    if not skip_dunntest:
        plot_statistical_test(runtimes_last_episode, 'steps',
                              dict(zip(indices, legend_values)), plot_title,
                              save_folder + f'dunnTest{suffix}.pdf')


def plot_deltaV(db, configs, location, episode, group_name,
                    legend_title, legend_values,  plot_title, save_folder):

    # get config  indices and then get data from db
    indices = [np.uint16(c[1:]) for c in configs.index]  # config numbers
    deltaV = load_deltaV(db, indices, location)

    # prepare save folder
    save_folder = os.path.join(save_folder , group_name, '')
    make_folder(save_folder)
    suffix = '' if group_name == '' else f'_{group_name}'

    # do the actual plotting
    plot_time_series(deltaV, 'episode', 'deltaV', legend_values,
                     'episode', 'deltaV', legend_title, plot_title,
                     save_folder + f'deltaV{suffix}', [0, 1, 0.1]
                     )


def plot_paths(title, config_folder, config_df, save_name):

    # first plot paths and then plot maze
    # create plot
    p = ggplot() + ggtitle(title)

    # plot paths
    num_rats = 100
    for id in range(num_rats):
        # check if file exists
        file_name = os.path.join(config_folder, f'r{id}-paths.bin')
        if not os.path.exists(file_name):
            continue

        # print(file_name, save_name)
        # open file and plot each path
        with open( file_name, 'rb') as file:
            for i in range(int(config_df['numStartingPositions'])):
                xy_df = pd.DataFrame(data=load_float_vector(file).reshape((-1, 2)), columns=["x", "y"])
                p = p + geom_path(aes(x='x', y='y'), data=xy_df, color='blue', alpha=1.0/num_rats)


    # plot maze
    maze_file = os.path.join(config_folder, '../../mazes', config_df['mazeFile'])
    walls, feeders, start_positions = parse_maze(maze_file)
    p = p + geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=walls, color='k')
    p = p + geom_point(aes(x='x', y='y'), data=feeders, color='r')
    p = p + coord_fixed(ratio = 1)

    # save plot
    ggsave(p, save_name, dpi=300)
