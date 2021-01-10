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


def format_scale(config):
    return f's{int(float(config["pcSizes"])*100):02d}'


def format_trace(config):
    return f't{float(config["traces"]):.1f}'


def format_nx(config):
    return f'nx{int(config["numX"]):02d}'


def format_maze(config):
    maze = ntpath.basename(config['mazeFile'])[1:-4]
    return f'M{maze}'

def format_pc_file(config):
    pc_file = ntpath.basename(config['pc_files'])[0:-4]
    return f'L{pc_file}'


def apply_formatters( config, formatters):
    return  '-'.join([f(config) for f in formatters])


def plot_config(experiment_folder, config, config_id):

    # check which experiment to plot
    experiment_name = ntpath.basename((ntpath.normpath(experiment_folder)))\
                            .split(sep='-')[0][10:]  # all experiments use syntax 'experimentN-...'

    # get folder names (create figure folder if necessary)
    config_folder = f'{experiment_folder}configs/{config_id}/'
    figure_folder = experiment_folder + 'figures/paths/'
    make_folder(figure_folder)

    # get format for configuration name
    e_formatters = {
        '1': [format_maze, format_trace, format_scale],
        '2': [format_maze, format_scale],
        '3': [format_maze, format_scale],
        '4': [format_maze, lambda c: f's{c["pcSizes"]}', lambda c: f't{c["traces"]}'],
        '5': [format_maze, format_trace, format_nx],
        '6': [format_maze, lambda c: f's{c["pcSizes"]}', lambda c: f't{c["traces"]}'],
        '7': [format_maze, format_pc_file, lambda c: f't{c["traces"]}']
    }
    config_title = apply_formatters(config, e_formatters[experiment_name])
    save_name = os.path.join(figure_folder, 'paths_' + config_title + '.pdf')

    # plot configuration

    plot_paths(config_title, config_folder, config, save_name)


def plot_experiment(folder, config_id):

    # load configs and connect to database
    configs = load_config_file(folder)

    if config_id is None:
        for index, config in configs.iterrows():
            plot_config(folder, config, index)
    else:
        plot_config(folder, configs.loc[config_id], config_id)


if __name__ == '__main__':
    folder_arg = os.path.join(sys.argv[1], '')
    config_arg = None if len(sys.argv) < 3 else sys.argv[2]
    # folder_arg = 'D:/JavaWorkspaceSCS/Multiscale-F2019/experiments/BICY2020_modified/logs/experiment1-traces/'
    plot_experiment(folder_arg, config_arg)

