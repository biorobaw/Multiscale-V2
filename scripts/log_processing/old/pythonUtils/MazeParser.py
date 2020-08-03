import xml.etree.ElementTree as ET
from functools import *


def parse_feeder(xml_feeder):
    fid = int(xml_feeder.get('id'))
    x = float(xml_feeder.get('x'))
    y = float(xml_feeder.get('y'))
    return [fid, x, y]


def parse_all_feeders(root):
    return [parse_feeder(xml_feeder) for xml_feeder in root.findall('feeder')]


def parse_wall(xml_wall):
    return [float(xml_wall.get(coord)) for coord in ['x1', 'y1', 'x2', 'y2']]


def parse_all_walls(xml_root):
    return [parse_wall(xml_wall) for xml_wall in xml_root.findall('wall')]


def parse_all_generators(xml_root):
    wall_sets = [generator_parsers[g.get('class')](g) for g in xml_root.findall('generator')]
    return reduce(lambda x, y: x+y, wall_sets)


def parse_rectangle(xml_rectangle):
    x1 = float(xml_rectangle.get('x1'))
    y1 = float(xml_rectangle.get('y1'))
    x2 = float(xml_rectangle.get('x2'))
    y2 = float(xml_rectangle.get('y2'))

    return [
        [x1, y1, x2, y1],
        [x2, y1, x2, y2],
        [x2, y2, x1, y2],
        [x1, y2, x1, y1]
    ]


generator_parsers = {'$(SCS).maze.mazes.Rectangle': parse_rectangle}


def parse_position(xml_position):
    return [float(xml_position.get(p)) for p in ['x', 'y']]


def parse_start_positions(xml_positions):
    return [parse_position(xml_pos) for xml_pos in xml_positions.findall('pos')]


def parse_maze(file):
    root = ET.parse(file).getroot()
    start_positions = parse_start_positions(root.find('startPositions'))
    walls = parse_all_walls(root) + parse_all_generators(root)
    feeders = parse_all_feeders(root)

    return walls, feeders, start_positions
