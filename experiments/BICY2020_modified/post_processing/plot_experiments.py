import git
import sys
import git
import os
import time
import tracemalloc
import sqlite3
import numpy as np
import ntpath


git_root = git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel")
sys.path.append(git_root)
from scripts.log_processing.plotting import *
layer_metrics_file = os.path.join(git_root, 'experiments/pc_layers/layer_metrics.csv')

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


def plot_experiment_11(figure_folder, configs, sample_rate, db):

    # toggle plots:
    plot_locally_uniform = True
    plot_non_uniform = True

    # normalize path to layers in configs dataframe:
    configs['pc_files'] = configs.pc_files.map( os.path.normpath )
    configs['pcs'] = configs.pc_files.map(lambda v : ntpath.basename(v)[0:-4])

    # layers of minimum coverage:
    min_layers = ['u04_40', 'u08_21', 'u12_14', 'u16_11', 'u20_09', 'u24_07', 'u28_06', 'u32_06', 'u36_06', 'u40_05', 'u44_05', 'u48_04', 'u52_04', 'u56_04']


    #########################################################################################################################################################
    # LOCALLY UNIFORM EXPERIMENT:
    #########################################################################################################################################################
    if plot_locally_uniform:
        folder_lu = os.path.join(figure_folder,'locally_uniform/')
        folder_lu_runtimes = os.path.join(folder_lu, 'runtimes/')
        make_folder(folder_lu)
        make_folder(folder_lu_runtimes)

        # function to plot boxplot
        def plot_box_plot(data, x_column, y_column, x_title, y_title, legend_title, plot_title, fill_cat, ylim):
            # print(data)
            p0 = ggplot(data, aes(x_column, y_column, fill=fill_cat )) \
                 + geom_jitter(alpha=0.3, position=position_jitterdodge(dodge_width=0.75), mapping=aes(group=fill_cat)) \
                 + geom_boxplot(alpha=0.7, notch=False, outlier_alpha=0) \
                 + labs(x=x_title, y=y_title, title=plot_title) \
                 + theme(axis_text_x=element_text(rotation=45, hjust=0.5)) \
                 + scale_fill_brewer(type="qual", palette=1, name=legend_title) \
                 + coord_cartesian(ylim=ylim)              
            return p0

        def plot_time_series(data, x_column, y_column, x_title, y_title, legend_title, plot_title, fill_cat, xlim, ylim):
            # print(data)
            p0 = ggplot(data, aes(x_column, y_column, color=fill_cat)) \
             + geom_line() \
             + labs(x=x_title, y=y_title, title=plot_title, caption='smt') \
             + coord_cartesian(xlim=xlim, ylim=ylim) \
             + scale_color_brewer(type="qual", palette=1, name=legend_title) 
            return p0


        for m in ['M0', 'M1']:
            
            print(f'PLOTTING LOCALLY UNIFORM: {m}')

            categories = ['original', 'goal', 'goal and gap']
            if m == 'M0':
                categories = categories[0:-1]

            # GET MAZE CONFIGS
            maze_configs = configs[configs.mazeFile.str.contains(m  + '.xml' )].copy()

            # GET CONFIGS ONLY FROM MIN LAYERS:
            maze_configs['pcs'] = maze_configs.pc_files.map(lambda v : ntpath.basename(v)[0:-4])
            min_layer_configs = maze_configs[maze_configs.pc_files.str.contains('|'.join(min_layers[4:]))]

            # GET CONFIGS FROM LOCALLY UNIFORM LAYERS
            locally_uniform_layers = maze_configs[maze_configs.pc_files.str.contains( 'lu')]

            # CONCAT RELEVANT CONFIGS
            experiment_configs = pd.concat([min_layer_configs, locally_uniform_layers])

            # CREATE INFORMATION FOR GROUPS:
            experiment_configs['base layer'] = experiment_configs.pcs.map(lambda l : re.findall('\d+', l)[-2])
            experiment_configs['legend groups'] = experiment_configs.pcs.map(lambda l : 'original' if l[0]=='u' else 'goal' if l[2] == '0' else 'goal and gap')

            for t in [0, 0.7]:
                traces_configs = experiment_configs[experiment_configs.traces == t].copy()

                location = -1
                num_episodes = traces_configs['numEpisodes'].max() / traces_configs['numStartingPositions'].max()
                last_episode = -sample_rate % num_episodes
                indices = [np.uint16(c[1:]) for c in traces_configs.index]  # config numbers

                # LOAD CONFIG SUMMARIES, ADD EXTRA FIELDS
                runtimes_last_episode = load_episode_runtimes(db, indices, location, last_episode)
                runtimes_last_episode['base layer'] = runtimes_last_episode.config.map(lambda c : traces_configs.loc['c'+str(c),'base layer'])
                runtimes_last_episode['legend groups'] = runtimes_last_episode.config.map(lambda c : traces_configs.loc['c'+str(c),'legend groups'])
                fill_cat = pd.Categorical(runtimes_last_episode['legend groups'], categories= categories)
                runtimes_last_episode = runtimes_last_episode.assign(fill_cat = fill_cat)


                group_name = f'{m}'
                plot_title = f'Maze {m[1:]} - Trace {t}'

                lims = [0, 1]
                p = plot_box_plot(runtimes_last_episode, 'base layer', 'steps', 'Base Layer', 'Extra Steps', 'Group', plot_title, fill_cat, lims)
                ggsave(p, folder_lu + f'Boxplots-{m}-T{int(t*10)}-l{lims[1]}.pdf', dpi=300, verbose = False)

                # plot runtimes:
                for base_layer, base_layer_configs in traces_configs.groupby(['base layer']):

                    plot_title = f'Maze {m[1:]} - Trace {t} - Base layer {base_layer}' 
                    ylims = [0, 2]
                    xlims = [0, 1000]
                    save_name = folder_lu_runtimes + f'runtimes-{m}-T{int(t*10)}-L{base_layer}-y{ylims[1]}-x{xlims[1]}.pdf'
                    print(f'    Plot layer: {base_layer}   -   file: {ntpath.basename(save_name)}')


                    indices = [np.uint16(c[1:]) for c in base_layer_configs.index]  # config numbers
                    erros_vs_episode_df = load_summaries(db, indices, location)
                    erros_vs_episode_df['base layer'] = erros_vs_episode_df.config.map(lambda c : base_layer_configs.loc['c'+str(c),'base layer'])
                    erros_vs_episode_df['legend groups'] = erros_vs_episode_df.config.map(lambda c : base_layer_configs.loc['c'+str(c),'legend groups'])
                    fill_cat = pd.Categorical(erros_vs_episode_df['legend groups'], categories= categories)
                    erros_vs_episode_df = erros_vs_episode_df.assign(fill_cat = fill_cat)

                    p = plot_time_series(erros_vs_episode_df, 'episode', 'steps' , 'Episode', 'Extra Steps', 'Group', plot_title, 'fill_cat', xlims, ylims )
                    ggsave(p, save_name, dpi=300, verbose = False)


    #########################################################################################################################################################
    # NON UNIFORM EXPERIMENT:
    #########################################################################################################################################################
    if plot_non_uniform:
        folder_nu = os.path.join(figure_folder,'non_uniform/')
        folder_nu_runtimes = os.path.join(folder_nu, 'runtimes/')
        make_folder(folder_nu)
        make_folder(folder_nu_runtimes)

        # GET LAYER METRICS 
        layer_metrics = pd.read_csv(layer_metrics_file)
        layer_metrics['layer'] = layer_metrics.layer.map(lambda l : os.path.normpath(os.path.join('experiments/pc_layers', l)) ) # normalize path and prepend location

        # PLOTTING FUNCTIONS FOR NON UNIFORM EXPERIMENT
        # BOXPLOT FUNCTION
        def plot_box_plot(data, x_column, y_column, x_title, y_title, plot_title, ylim, box_colors):
            # print(data)
            p0 = ggplot(data, aes(x_column, y_column )) \
                 + geom_jitter(alpha=0.3) \
                 + geom_boxplot(alpha=0.7, notch=False, outlier_alpha=0, color = box_colors ) \
                 + labs(x=x_title, y=y_title, title=plot_title) \
                 + theme(axis_text_x=element_text(rotation=45, hjust=1)) \
                 + coord_cartesian(ylim=ylim)              
            return p0

        def plot_time_series(data, x_column, y_column, x_title, y_title, legend_title, plot_title, fill_cat, xlim, ylim):
            # print(data)
            p0 = ggplot(data, aes(x_column, y_column, color=fill_cat)) \
             + geom_line() \
             + labs(x=x_title, y=y_title, title=plot_title, caption='smt') \
             + coord_cartesian(xlim=xlim, ylim=ylim) \
             + scale_color_discrete(name=legend_title)
             # + scale_color_brewer(type="seq", palette=1, name=legend_title) 
            return p0

        for m in ['M0', 'M1', 'M8']:

            print(f'PLOTTING NON UNIFORM: {m}')

            # GET MAZE CONFIGS RELEVANT TO EXPERIMENT
            maze_configs = configs[configs.mazeFile.str.contains(m + '.xml')]
            maze_configs = maze_configs[maze_configs.pc_files.str.contains('|'.join(['non_uniform'] + min_layers))].copy()


            # CREATE INFORMATION FOR GROUPS:
            experiment_configs = pd.merge(maze_configs.reset_index(), layer_metrics, left_on='pc_files', right_on='layer', how='left').set_index('config')
            alias = lambda l : l[0:3] if l[0] == 'u' else 'nu'
            cells = lambda r : r['number of cells']
            experiment_configs['layer_alias'] = experiment_configs.apply( lambda r : f'{alias(r["pcs"])} ({cells(r)})' , axis = 1 )


            for t in [0, 0.7]:
                print(f'   Trace {t}')
                # GET TRACE CONFIGS 
                trace_configs = experiment_configs[experiment_configs.traces == t]
                indices = [np.uint16(c[1:]) for c in trace_configs.index]  # config numbers

                # DEFINE ORDER OF GROUPS
                groups = list(trace_configs.layer_alias.values)
                position = 5
                categories = groups[0:position] + [groups[-1]] + groups[position:-1]


                # GET DATA FROM LAST EPISODE:
                location = -1
                num_episodes = trace_configs['numEpisodes'].max() / trace_configs['numStartingPositions'].max()
                last_episode = -sample_rate % num_episodes
                runtimes_last_episode = load_episode_runtimes(db, indices, location, last_episode)
                runtimes_last_episode['layer_alias'] = runtimes_last_episode.config.map(lambda c : trace_configs.loc[f'c{c}','layer_alias'])                
                runtimes_last_episode['categories'] = pd.Categorical(runtimes_last_episode.layer_alias, categories= categories)

                # GET RUNTIMES
                erros_vs_episode_df = load_summaries(db, indices, location)
                erros_vs_episode_df['layer_alias'] = erros_vs_episode_df.config.map(lambda c : trace_configs.loc[f'c{c}','layer_alias'])
                erros_vs_episode_df['categories'] = pd.Categorical(erros_vs_episode_df.layer_alias, categories=categories)


                # PLOT BOXPLOTS
                plot_title = f'Maze {m[1:]} - Trace {t}'
                lims = [0, 1]

                box_plot_colors = ['black' for i in range(len(categories))]
                box_plot_colors[position] = 'red'

                save_name = f'Boxplots-{m}-T{int(t*10)}-l{lims[1]}.pdf'
                print(f'      PLOT: BOXPLOT - {save_name}')
                p = plot_box_plot(runtimes_last_episode, 'categories', 'steps', 'Layer', 'Extra Steps', plot_title, lims, box_plot_colors)
                ggsave(p, folder_nu + save_name, dpi=300, verbose = False)



                # plot runtimes:
                plot_title = f'Maze {m[1:]} - Trace {t}'
                ylims = [0, 1]
                xlims = [0, 10000]

                save_name = f'runtimes-{m}-T{int(t*10)}-y{ylims[1]}-x{xlims[1]}.pdf'
                print(f'      PLOT: RUNTIME - {save_name}')
                p = plot_time_series(erros_vs_episode_df, 'episode', 'steps' , 'Episode', 'Extra Steps', 'Group', plot_title , 'categories', xlims, ylims )
                ggsave(p, folder_nu_runtimes + save_name, dpi=300, verbose = False)
                


    # # first plot locally uniform experiment: 
    # # for each original layer (bigger than 16), compare single layer + added cells at goal + added cells at gap

    # print('Plotting locally uniform experiment')
    # folder_lu = os.path.join(figure_folder,'locally_uniform/')
    # make_folder(folder_lu)
    # for m in ['M0', 'M1']:
    #     maze_configs = configs[configs.mazeFile.str.contains(m)]
    #     m_min_uniform_configs = maze_configs[pc_files.std.contains]





    # # get layer metrics
    # layer_metrics = pd.read_csv(os.path.join(git_root,'experiments/pc_layers/layer_metrics.csv'))


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
    experiment_map['11'] = ( plot_experiment_11, 5)

    # plot the experiment
    e = experiment_map[experiment_name]
    fun = e[0]
    sample_rate = e[1]
    fun(figure_folder, configs, sample_rate, db)


if __name__ == '__main__':
    folder_arg = sys.argv[1]
    # folder_arg = 'D:/JavaWorkspaceSCS/Multiscale-F2019/experiments/BICY2020_modified/logs/experiment1-traces/'
    plot_experiment(folder_arg)
