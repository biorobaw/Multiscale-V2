import xml.etree.ElementTree as ET
from pythonUtils.MazeParser import *
from plotnine import *
import pandas as pd
import os
import math
from pythonUtils.VariableLoader import *

# this file defines functionality for:
#       loading mazes
#       plotting walls
#       plotting feeders
#       plotting starting locations
#       plotting cells (circles)


def get_pc_layer_constants(width, height, radius):
    nx = math.ceil((width / (2 * radius) + 1) * math.sqrt(2) - 1)
    ny2 = math.ceil((height / (2*radius) + 1) * math.sqrt(2) - 1)
    ny = math.floor(nx * height / width)
    nxy = nx * ny
    wx = (width + 2 * radius) / (nx + 1)
    wy = (height + 2 * radius) / (ny + 1)
    return nx, ny, ny2, nxy, wx, wy

def load_maze(xml_file):
    root = ET.parse(xml_file).getroot()

    start_positions = pd.DataFrame(parse_start_positions(root.find('startPositions')), columns=['x', 'y'])
    walls = parse_all_walls(root)
    walls += parse_rectangle(root.find('mazeElement').find('params'))
    walls = pd.DataFrame(walls, columns=['x1', 'y1', 'x2', 'y2'])
    feeder = parse_feeder(root.find('feeder'))
    feeder = pd.DataFrame([feeder], columns=['id', 'x', 'y'])

    return walls, feeder, start_positions


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


def plot_mazes(mazes_folder):
    # list of experiment files
    maze_files = get_list_of_mazes(mazes_folder)

    if not os.path.exists('images/mazes/'):
        os.makedirs('images/mazes/')

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
        ggsave(plot=p, filename='images/mazes/{}.pdf'.format(os.path.basename(m).strip('.xml')), dpi=100)


def plot_pc_placement_example(radius, width, height):
    # plot example of pc placement
    m_walls, m_feeders, m_start_positions = load_maze('mazes/M0.xml')
    nx = math.ceil((width / (2 * radius) + 1) * math.sqrt(2) - 1)
    ny = math.floor(nx * height / width)
    nxy = nx * ny
    wx = (width + 2 * radius) / (nx + 1)
    wy = (height + 2 * radius) / (ny + 1)
    centers = [[wx * (i % nx + 1) - radius - width / 2, wy * (i // nx + 1) - radius - height / 2] for i in
               range(0, nxy)]
    centers_df = pd.DataFrame(centers, columns=['x', 'y'])

    p = ggplot()
    p = plot_walls(p, m_walls) + coord_fixed(ratio=1)
    p = plot_circles(p, centers, radius)
    p = p + geom_point(aes('x', 'y'), data=centers_df, color='red')
    p = p + ggtitle('Sample PC layer - Scale={:.2f} nx={}'.format(radius, nx))
    ggsave(plot=p, filename='images/pcs/sample-scale{:.2f}-nx{}.png'.format(radius, nx), dpi=100)


if __name__ == '__main__':

    # plot_mazes('mazes/')
    # plot_pc_placement_example(radius=0.12, width=2.2, height=3.0)
    plot_pc_placement_example(radius=0.56, width=2.2, height=3.0)




