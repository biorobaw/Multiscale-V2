from ..utils.MazeParser import *
from plotnine import *
import math
import pandas as pd
from data_loader import *

# this file defines functionality for:
#       loading mazes
#       plotting walls
#       plotting feeders
#       plotting starting locations
#       plotting cells (circles)
#       also, main function plot mazes and sample pc layers


def get_pc_layer_constants(width, height, radius):
    nx = math.ceil((width / (2 * radius) + 1) * math.sqrt(2) - 1)
    ny2 = math.ceil((height / (2*radius) + 1) * math.sqrt(2) - 1)
    ny = math.floor(nx * height / width)
    nxy = nx * ny
    wx = (width + 2 * radius) / (nx + 1)
    wy = (height + 2 * radius) / (ny + 1)
    return nx, ny, ny2, nxy, wx, wy


def load_maze(xml_file_name):
    walls, feeders, start_positions = parse_maze(xml_file_name)
    start_positions_df = pd.DataFrame(start_positions, columns=['x', 'y'])
    walls_df = pd.DataFrame(walls, columns=['x1', 'y1', 'x2', 'y2'])
    feeders_df = pd.DataFrame(feeders, columns=['id', 'x', 'y'])

    return walls_df, feeders_df, start_positions_df


def plot_walls(plot, walls):
    return plot + geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=walls)


def plot_starting_positions(plot, positions,delta_y=0.03):
    return plot + geom_point(aes(x='x', y='y'), data=positions, color='red', size=4) \
           + geom_text(aes(x='x', y='y', label='index'), va='bottom', nudge_y=delta_y,
                       data=positions.reset_index(), size=18)


def plot_feeders(plot, feeders, delta_y=0.03):
    aux = plot + geom_point(aes(x='x', y='y'), data=feeders, color='blue', size=4)
    if 'tag' in feeders:
        aux = aux + geom_text(aes(x='x', y='y', label='tag'), va='bottom', nudge_y=delta_y, data=feeders, size=18)
    return aux


def plot_circles(plot, pcs, radius):
    num_points = 100
    xs = [radius*math.cos(2*math.pi*i/num_points) for i in range(num_points)]
    ys = [radius*math.sin(2*math.pi*i/num_points) for i in range(num_points)]
    circle = pd.DataFrame({'x': xs, 'y': ys})
    aux = plot
    for i in range(len(pcs)):
        data = circle+pcs[i]
        aux = aux + geom_path(aes(x='x', y='y'), data=data)
    return aux


def plot_mazes(mazes_folder, output_folder):
    # list of experiment files
    maze_files = get_list_of_mazes(mazes_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # plot each maze
    for m in maze_files:
        m_walls, m_feeders, m_start_positions = load_maze(mazes_folder + m)

        m_feeders['tag'] = 'Feeder'

        print(m_start_positions)
        p = ggplot()
        p = plot_walls(p, m_walls) + coord_fixed(ratio=1)
        p = plot_starting_positions(p, m_start_positions)
        p = plot_feeders(p, m_feeders) # + ggtitle(os.path.basename(m))
        p = p + xlab('') + ylab('') + theme_grey(base_size = 18) # + \
            # theme(legend_title=element_blank())
        ggsave(plot=p, filename=output_folder + '{}.pdf'.format(os.path.basename(m).strip('.xml')), dpi=100)


def plot_pc_placement_example(maze, output_folder, radius, minx, maxx, numx, miny, maxy, numy):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # plot example of pc placement
    m_walls, m_feeders, m_start_positions = load_maze(maze)
    dx = (maxx-minx)/numx
    dy = (maxy-miny)/numy
    centers = [[minx + dx * (i % numx), miny + dy * (i // numx + 1)]
               for i in range(0, numx*numy)]
    centers_df = pd.DataFrame(centers, columns=['x', 'y'])

    p = ggplot()
    p = plot_walls(p, m_walls) + coord_fixed(ratio=1)
    p = plot_circles(p, centers, radius)
    p = p + geom_point(aes('x', 'y'), data=centers_df, color='red')
    p = p + ggtitle('Sample PC layer - Scale={:.2f}'.format(radius))
    ggsave(plot=p, filename=output_folder + 'sample-r{:.2f}-mx{}-Mx{}-nx{}-my{}-My{}-ny{}.png'
           .format(radius, minx, maxx, numx, miny, maxy, numy), dpi=300)


if __name__ == '__main__':
    base_log_folder = '../../logs/development/old_tests/'
    plot_mazes(base_log_folder + 'mazes/', base_log_folder + 'images/mazes/')
    background_maze = base_log_folder + 'mazes/M0.xml'
    plot_pc_placement_example(background_maze, base_log_folder + 'images/pcs/', 0.04, -1.084, 1.084, 40, -1.484, 1.484, 54)




