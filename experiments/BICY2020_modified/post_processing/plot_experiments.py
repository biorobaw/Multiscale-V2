import git
import sys
import git
import os
import time
import tracemalloc
import sqlite3

sys.path.append(git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel"))
from scripts.log_processing.plotting import *
from scripts.log_processing.data_loader import *


def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def plot_experiment_traces(folder, figure_folder, configs, db):
    """ for each scale, grouping by trace value:
            plot runtimes
            box plot of last episode
            dunn test of last episode
    """

    # PARAMETERS:
    location = -1  # we will only plot geometric mean data (represented with location -1)
    num_episodes = configs['numEpisodes'].max() / configs['numStartingPositions'].max()
    sample_rate  = 5  # rate at which episodes where sampled to reduce DB size
    last_episode = -sample_rate % num_episodes

    # plot each scale separately
    for scale, sub_configs in configs.groupby(['pcSizes']):
        print('plotting scale: ', scale)
        # get indices and format text for the plots
        indices = [np.uint8(c[1:]) for c in sub_configs.index] # config numbers
        scale_str = "{0:.2f}".format(scale)
        traces = sub_configs.traces.map("{0:.2f}".format)

        # prepare folder
        scale_folder = figure_folder + f's{scale_str}/'
        make_folder(scale_folder)


        # plot summary runtimes
        summaries = load_summaries(db, indices, location)
        save_name = scale_folder + 'runtimes_scale-{}'.format(scale_str)

        plot_time_series(summaries, 'episode', 'steps', traces,
                         'episode', 'optimality ratio', 'Trace', f"scale {scale_str}",
                         save_name, [0, 1.3, 4]
                         )

        # plot box plots of last episode and dunn tests
        runtimes_last_episode = load_episode_runtimes(db, indices, location, last_episode)
        save_name = scale_folder + f'boxplot_s{scale_str}'
        plot_box_plot(runtimes_last_episode, 'steps', traces,
                      'trace', 'optimality ratio', f'scale {scale_str}',
                      save_name, [0, 1.3, 4])

        save_name = scale_folder + f'dunnTest_s{scale_str}.pdf'
        config_names = dict(zip(indices, traces))
        plot_statistical_test(runtimes_last_episode, 'steps', config_names, '', save_name)  # skipping title


if __name__ == '__main__':
    # get experiment folder
    folder = os.path.join(sys.argv[1], '')
    # folder = 'D:/JavaWorkspaceSCS/Multiscale-F2019/experiments/BICY2020_modified/logs/experiment1-traces/'

    # create figures folder
    figure_folder = folder + 'figures/'
    make_folder(figure_folder)

    # load configs and connect to database
    configs = load_config_file(folder)
    db = sqlite3.connect(folder + 'experiment_results.sqlite')

    # plot the experiment
    plot_experiment_traces(folder, figure_folder, configs, db)