import scikit_posthocs as sp
from plotnine import *

"""
   This file is to be called after processAllConfigs,
   it creates the plots for the multi_scale_memory model 
   that require information from multiple configurations   
"""


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
        ggsave(p, file_name + '-lim{:02d}.pdf'.format(int(lim)), dpi=300)


def plot_time_series(data, x_column, y_column, group_labels, x_title, y_title, legend_title, plot_title, save_name, zoom_levels= [0, 2.5, 5]):
    p0 = ggplot(data, aes(x_column, y_column, color='factor(config)', group='config')) \
         + geom_line() \
         + labs(x=x_title, y=y_title, title=plot_title, caption='smt') \
         + scale_color_discrete(name=legend_title, labels=group_labels)
    zoom_and_save(p0, zoom_levels, save_name)


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












