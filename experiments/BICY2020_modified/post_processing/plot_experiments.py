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


def plot_experiment_traces_and_scales_per_maze(figure_folder, configs, sample_rate, db):
    """ for each scale, grouping by trace value:
            plot runtimes
            box plot of last episode
            dunn test of last episode
    """

    # PARAMETERS:
    location = -1  # we will only plot geometric mean data (represented with location -1)
    num_episodes = configs['numEpisodes'].max() / configs['numStartingPositions'].max()
    last_episode = -sample_rate % num_episodes

    # for each maze
    for maze, maze_configs in configs.groupby(['mazeFile']):

        maze = ntpath.basename(maze)[1:-4]
        print('plotting maze: ', maze)

        maze_figure_folder = figure_folder + 'M' + maze +'/'
        make_folder(maze_figure_folder)

        # plot each scale separately
        for r, sub_configs in maze_configs.groupby(['pcSizes']):
            # get indices and format text for the plots
            # nx_str = "{0:.2f}".format(scale)  # convert to string and format
            print('plotting r: ', r)

            # plot titles and legends:

            group_name    = f's{r:.2f}'
            legend_title  = 'Traces'
            legend_values = sub_configs.traces.map("{0:.1f}".format)
            plot_title    = f"Maze {maze} - PC radius {int(r*100)}cm"

            plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                        legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, sub_configs, location, last_episode, group_name,
                                        legend_title, legend_values, plot_title, maze_figure_folder)

        # plot each scale separately
        for trace, sub_configs in maze_configs.groupby(['traces']):
            # get indices and format text for the plots
            # nx_str = "{0:.2f}".format(scale)  # convert to string and format
            print('plotting trace: ', trace)

            # plot titles and legends:

            group_name = f't{trace:.1f}'
            legend_title = 'PC Radius (cm)'
            legend_values = (sub_configs.pcSizes * 100).astype(int).astype(str)
            plot_title = f"Maze {maze} - Trace {trace:.1f}"

            plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                            legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, sub_configs, location, last_episode, group_name,
                        legend_title, legend_values, plot_title, maze_figure_folder)

def plot_experiment_traces_and_nx_per_maze(figure_folder, configs, sample_rate, db):
    """ for each scale, grouping by trace value:
            plot runtimes
            box plot of last episode
            dunn test of last episode
    """

    # PARAMETERS:
    location = -1  # we will only plot geometric mean data (represented with location -1)
    num_episodes = configs['numEpisodes'].max() / configs['numStartingPositions'].max()
    last_episode = -sample_rate % num_episodes

    # for each maze
    for maze, maze_configs in configs.groupby(['mazeFile']):

        maze = ntpath.basename(maze)[1:-4]
        print('plotting maze: ', maze)

        maze_figure_folder = figure_folder + 'M' + maze +'/'
        make_folder(maze_figure_folder)

        # plot each scale separately
        for nx, sub_configs in maze_configs.groupby(['numX']):
            # get indices and format text for the plots
            # nx_str = "{0:.2f}".format(scale)  # convert to string and format
            print('plotting nx: ', nx)

            # plot titles and legends:

            group_name    = f'nx{nx}'
            legend_title  = 'Traces'
            legend_values = sub_configs.traces.map("{0:.1f}".format)
            plot_title    = f"Maze {maze} - Columns {nx}"

            plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                        legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, sub_configs, location, last_episode, group_name,
                                        legend_title, legend_values, plot_title, maze_figure_folder)

        # plot each scale separately
        for trace, sub_configs in maze_configs.groupby(['traces']):
            # get indices and format text for the plots
            # nx_str = "{0:.2f}".format(scale)  # convert to string and format
            print('plotting trace: ', trace)

            # plot titles and legends:

            group_name = f't{trace:.1f}'
            legend_title = 'Columns'
            legend_values = sub_configs.numX.map("{}".format)
            plot_title = f"Maze {maze} - Trace {trace:.1f}"

            plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                            legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, sub_configs, location, last_episode, group_name,
                        legend_title, legend_values, plot_title, maze_figure_folder)

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

        plot_deltaV(db, sub_configs, location, last_episode, group_name,
                    legend_title, legend_values, plot_title, figure_folder)


def plot_experiment4_extraAtFeeder(figure_folder, configs, sample_rate, db):
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
    for maze, sub_configs1 in configs.groupby(['mazeFile']):
        # get indices and format text for the plots
        maze = ntpath.basename(maze)[1:-4]
        print('plotting maze: ', maze)

        maze_figure_folder = figure_folder + 'M' + maze + '/'
        make_folder(maze_figure_folder)

        # plot each scale separately
        for trace, sub_configs in sub_configs1.groupby(['traces']):
            # get indices and format text for the plots
            # nx_str = "{0:.2f}".format(scale)  # convert to string and format
            print('plotting trace: ', trace)

            # plot titles and legends:

            group_name = f'M{maze}-t{trace}'
            legend_title = 'PC radius (cm)'
            legend_values = sub_configs.pcSizes  # (sub_configs.pcSizes * 100).map("{0:.2f}".format)
            plot_title = f"Maze {maze} - Trace {trace}"

            plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                            legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, sub_configs, location, last_episode, group_name,
                        legend_title, legend_values, plot_title, maze_figure_folder)



def plot_experiment7(figure_folder, configs, sample_rate, db):
    """
    plot all
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
    for maze, maze_configs in configs.groupby(['mazeFile']):
        # get indices and format text for the plots
        maze = ntpath.basename(maze)[1:-4]
        print('plotting maze: ', maze)

        maze_figure_folder = figure_folder + 'M' + maze +'/'
        make_folder(maze_figure_folder)



        # group by trace:
        for trace, sub_configs in maze_configs.groupby(['traces']):

            group_name = f't{trace:.1f}'
            legend_title = 'Layer'
            legend_values = sub_configs.pc_files.map(format_pc_file)
            plot_title = f"Maze {maze} - trace {trace:.1f}"

            plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                            legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, sub_configs, location, last_episode, group_name,
                        legend_title, legend_values, plot_title, maze_figure_folder)

        # group by layer
        for layer, layer_configs in maze_configs.groupby(['pc_files']):

            group_name = f'L{format_pc_file(layer)}'
            legend_title = 'Trace'
            legend_values = layer_configs.traces.map("{0:.1f}".format)
            plot_title = f"Maze {maze} - Trace {trace:.1f}"

            plot_runtimes_boxplots_dunntest(db, layer_configs, location, last_episode, group_name,
                                            legend_title, legend_values, plot_title, maze_figure_folder)

            plot_deltaV(db, layer_configs, location, last_episode, group_name,
                        legend_title, legend_values, plot_title, maze_figure_folder)

        # for each layer

        # plot titles and legends:


def plot_experiment_8(figure_folder, configs, sample_rate, db):

    # PARAMETERS:
    location = -1  # we will only plot geometric mean data (represented with location -1)
    num_episodes = configs['numEpisodes'].max() / configs['numStartingPositions'].max()
    last_episode = -sample_rate % num_episodes

    # plot each numnber of obstacles separatedly:
    obstacle_figure_folder = figure_folder + 'obstacles/'
    make_folder(obstacle_figure_folder)

    for num_obstacles, sub_configs in configs.groupby(['numObstacles']):
        # get indices and format text for the plots
        print('obstacles: ', num_obstacles)

        group_name = f'o{num_obstacles}'
        legend_title = 'Maze'
        legend_values = sub_configs.mazeFile.map(format_pc_file) 
        plot_title = f"Obstacles {num_obstacles}"

        plot_runtimes_boxplots_dunntest(db, sub_configs, location, last_episode, group_name,
                                        legend_title, legend_values, plot_title, obstacle_figure_folder)




def format_pc_file(file_name):
    # WARNING: also used for maze, if no longer useful will need separate funcion
    pc_file = ntpath.basename(file_name)[0:-4]
    return f'{pc_file}'


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
    experiment_map['1'] = ( plot_experiment_traces_and_scales_per_maze, 5 )
    experiment_map['2'] = ( plot_scale_experiment                     , 5 )
    experiment_map['3'] = ( plot_scale_experiment                     , 5 )
    experiment_map['4'] = ( plot_experiment4_extraAtFeeder            , 5 )
    experiment_map['5'] = ( plot_experiment_traces_and_nx_per_maze    , 10)
    experiment_map['6'] = ( plot_experiment4_extraAtFeeder            , 5 )
    experiment_map['7'] = ( plot_experiment7, 5)
    experiment_map['8'] = ( plot_experiment_8, 5)
    experiment_map['9'] = ( plot_experiment_8, 5)

    # plot the experiment
    e = experiment_map[experiment_name]
    fun = e[0]
    sample_rate = e[1]
    fun(figure_folder, configs, sample_rate, db)


if __name__ == '__main__':
    folder_arg = sys.argv[1]
    # folder_arg = 'D:/JavaWorkspaceSCS/Multiscale-F2019/experiments/BICY2020_modified/logs/experiment1-traces/'
    plot_experiment(folder_arg)
