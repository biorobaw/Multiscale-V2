import xml.etree.ElementTree as ET
from functools import *
import pandas as pd


def parse_feeder(xml_feeder):
    fid = int(xml_feeder.get('id'))
    x = float(xml_feeder.get('x'))
    y = float(xml_feeder.get('y'))
    return pd.DataFrame(data=[[fid, x, y]], columns=['fid', 'x', 'y'])


def parse_all_feeders(root):
    return pd.concat([pd.DataFrame(columns=['fid', 'x', 'y'])] + [parse_feeder(xml_feeder) for xml_feeder in root.findall('feeder')]).reset_index(drop=True)


def parse_wall(xml_wall):
    data = [[float(xml_wall.get(coord)) for coord in ['x1', 'y1', 'x2', 'y2']]]
    return pd.DataFrame(data=data, columns=['x1', 'y1', 'x2', 'y2'])


def parse_all_walls(xml_root):
    return pd.concat([pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'])]  + [parse_wall(xml_wall) for xml_wall in xml_root.findall('wall')]).reset_index(drop=True)


def parse_all_generators(xml_root):
    wall_sets = [generator_parsers[g.get('class')](g) for g in xml_root.findall('generator')]
    return pd.concat([pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'])] + wall_sets).reset_index(drop=True)


def parse_rectangle(xml_rectangle):
    x1 = float(xml_rectangle.get('x1'))
    y1 = float(xml_rectangle.get('y1'))
    x2 = float(xml_rectangle.get('x2'))
    y2 = float(xml_rectangle.get('y2'))

    data = [
        [x1, y1, x2, y1],
        [x2, y1, x2, y2],
        [x2, y2, x1, y2],
        [x1, y2, x1, y1]
    ]
    return pd.DataFrame(data=data, columns=['x1', 'y1', 'x2', 'y2'])


generator_parsers = {'$(SCS).maze.mazes.Rectangle': parse_rectangle}


def parse_position(xml_position):
    return pd.DataFrame(data=[[float(xml_position.get(p)) for p in ['x', 'y']]], columns=['x','y'])


def parse_start_positions(xml_positions):
    if xml_positions is None:
        return pd.DataFrame(columns=['x', 'y', 'w'])
    return pd.concat([pd.DataFrame(columns=['x', 'y', 'w'])] + [parse_position(xml_pos) for xml_pos in xml_positions.findall('pos')]).reset_index(drop=True)


def parse_maze(file):
    root = ET.parse(file).getroot()
    start_positions = parse_start_positions(root.find('startPositions'))
    walls = pd.concat([parse_all_walls(root), parse_all_generators(root)]).reset_index(drop=True)
    feeders = parse_all_feeders(root)

    return walls, feeders, start_positions
