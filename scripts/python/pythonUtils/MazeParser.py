

def parse_feeder(xml_feeder):
    fid = int(xml_feeder.find('id').text)
    x = float(xml_feeder.find('x').text)
    y = float(xml_feeder.find('y').text)
    return [fid, x, y]


def parse_all_feeders(root):
    return [parse_feeder(xml_feeder) for xml_feeder in root.findall('feeder')]


def parse_wall(xml_wall):
    x1 = float(xml_wall.find('x1').text)
    x2 = float(xml_wall.find('x2').text)
    y1 = float(xml_wall.find('y1').text)
    y2 = float(xml_wall.find('y2').text)
    return [x1, y1, x2, y2]


def parse_all_walls(xml_root):
    return [parse_wall(xml_wall) for xml_wall in xml_root.findall('wall')]


def parse_rectangle(xml_rectangle):
    x1 = float(xml_rectangle.find('x1').text)
    x2 = float(xml_rectangle.find('x2').text)
    y1 = float(xml_rectangle.find('y1').text)
    y2 = float(xml_rectangle.find('y2').text)

    return [
        [x1, y1, x2, y1],
        [x2, y1, x2, y2],
        [x2, y2, x1, y2],
        [x1, y2, x1, y1]
    ]


def parse_position(xml_position):
    return [float(f) for f in xml_position.text.split(',')[0:2]]


def parse_start_positions(xml_positions):
    return [parse_position(xml_pos) for xml_pos in xml_positions.findall('pos')]

