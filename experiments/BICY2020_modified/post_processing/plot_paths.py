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


def apply_formatters( config, formatters):
    return  '-'.join([f(config) for f in formatters])


def plot_experiment(folder):
    # get experiment folder
    folder = os.path.join(sys.argv[1], '')

    # load configs and connect to database
    configs = load_config_file(folder)

    # create figures folder
    figure_folder = folder + 'figures/paths/'
    make_folder(figure_folder)

    # plot the experiment
    experiment_name = ntpath.basename((ntpath.normpath(folder)))\
                            .split(sep='-')[0][10:]  # all experiments use syntax 'experimentN-...'

    experiment_name = '1'
    e_formatters = {
        '1': [format_maze, format_trace, format_scale],
        '2': [format_maze, format_scale],
        '3': [format_maze, format_scale],
        '4': [format_maze, lambda c: f's{c["pcSizes"]}'],
        '5': [format_maze, format_trace, format_nx],
        '6': [format_maze, lambda c: f's{c["pcSizes"]}']
    }

    for index, config in configs.iterrows():
        format = apply_formatters(config, e_formatters[experiment_name])
        plot_title = format
        config_folder = f'{folder}configs/{index}/'
        save_name = os.path.join(figure_folder, 'paths_' + format + '.pdf')
        plot_paths(plot_title, config_folder , config, save_name)

if __name__ == '__main__':
    folder_arg = sys.argv[1]
    # folder_arg = 'D:/JavaWorkspaceSCS/Multiscale-F2019/experiments/BICY2020_modified/logs/experiment1-traces/'
    plot_experiment(folder_arg)