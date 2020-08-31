import git
import sys
import git
import os
import time
import tracemalloc
import sqlite3
import numpy as np
import ntpath

sys.path.append(git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel"))
from scripts.log_processing.plotting import *


def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def plot_experiment_traces(figure_folder, configs, sample_rate, db):
    """ for each scale, grouping by trace value:
            plot runtimes
            box plot of last episode
            dunn test of last episode
    """

    # PARAMETERS:
    location = -1  # we will only plot geometric mean data (represented with location -1)
    num_episodes = configs['numEpisodes'].max() / configs['numStartingPositions'].max()
    last_episode = -sample_rate % num_episodes

    # plot each scale separately
    for scale, sub_configs in configs.groupby(['pcSizes']):
        # get indices and format text for the plots
        scale_str = "{0:.2f}".format(scale)  # convert to string and format
        print('plotting scale: ', scale)

        # plot titles and legends:

        group_name    = f's{scale_str}'
        legend_title  = 'Trace'
        legend_values = sub_configs.traces.map("{0:.2f}".format)
        plot_title    = f"Scale {scale_str}"

        plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                    legend_title, legend_values, plot_title, figure_folder)

        plot_deltaV(db, sub_configs, location, last_episode, group_name,
                                    legend_title, legend_values, plot_title, figure_folder)


def plot_scale_experiment(figure_folder, configs, sample_rate, db):
    """
    for each maze, grouping by scale
    :param folder:
    :param figure_folder:
    :param configs:
    :param db:
    :return:
    """

    # PARAMETERS:
    location = -1  # we will only plot geometric mean data (represented with location -1)
    num_episodes = configs['numEpisodes'].max() / configs['numStartingPositions'].max()
    last_episode = -sample_rate % num_episodes

    # plot each scale separately
    for maze, sub_configs in configs.groupby(['mazeFile']):
        # get indices and format text for the plots
        maze = ntpath.basename(maze)[1:-4]
        print('plotting maze: ', maze)

        # plot titles and legends:

        group_name = f'M{maze}'
        legend_title = 'PC radius (cm)'
        legend_values = (sub_configs.pcSizes * 100).map("{0:.2f}".format)
        plot_title = f"Maze {maze}"

        plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                        legend_title, legend_values, plot_title, figure_folder)

def plot_experiment(folder):
    # get experiment folder
    folder = os.path.join(sys.argv[1], '')

    # load configs and connect to database
    configs = load_config_file(folder)
    db = sqlite3.connect(folder + 'experiment_results.sqlite')

    # create figures folder
    figure_folder = folder + 'figures/'
    make_folder(figure_folder)

    # plot the experiment
    experiment_name = ntpath.basename((ntpath.normpath(folder)))\
                            .split(sep='-')[0][10:]  # all experiments use syntax 'experimentN-...'

    experiment_map = {}
    experiment_map['1'] = ( plot_experiment_traces, 5)
    experiment_map['2'] = ( plot_scale_experiment,  5)
    experiment_map['3'] = ( plot_scale_experiment,  5)

    # plot the experiment
    e = experiment_map[experiment_name]
    fun = e[0]
    sample_rate = e[1]
    fun(figure_folder, configs, sample_rate, db)


if __name__ == '__main__':
    folder_arg = sys.argv[1]
    # folder_arg = 'D:/JavaWorkspaceSCS/Multiscale-F2019/experiments/BICY2020_modified/logs/experiment1-traces/'
    plot_experiment(folder_arg)