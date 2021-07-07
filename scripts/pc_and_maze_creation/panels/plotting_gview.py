import sys
from PyQt5.Qt import QApplication, QLabel, QMainWindow, \
                            QWidget, QVBoxLayout, QTableWidget, \
                            QHeaderView, QCheckBox, QTableWidgetItem, \
                            QItemDelegate, QLineEdit, QDoubleSpinBox, QPushButton, \
                            QSpacerItem, QHBoxLayout, QSizePolicy, QFileDialog, \
                            QGraphicsView, QGraphicsScene, QPalette, QColor, \
                            QDoubleValidator, QBrush, QPen, QGraphicsEllipseItem, \
                            QGraphicsRectItem, QGraphicsTextItem, QPen, QLineF, \
                            QRectF, Qt, QPainter, QTransform, QKeyEvent, QWheelEvent, \
                            QMouseEvent, QMouseEvent, QGraphicsItem

from data.PC import PlaceCell
from data.Wall import Wall

class GViewPlotting(QGraphicsView):

    graphics = {}  # hash to store graphic elements
    pc_from_graphic = {}
    wall_from_graphics = {}
    feeder_from_graphics = {}
    start_pos_from_graphics = {}
    view_rect = QRectF(-1, -1, 2, 2)  # user defined rectangle of scene coordinates
    auto_fit = True

    start_pos_drawing_radius = 0.02
    feeder_drawing_radius = 0.02


    def __init__(self, *args, **kwargs):
        super(GViewPlotting, self).__init__(*args, **kwargs)

        self.dragging_pc = None
        self.dragging_start_pos = None
        self.dragging_wall = None
        self.path_graphics = []

        # remove scroll bars
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # create empty scene
        scene = QGraphicsScene(self)
        self.setScene(scene)

        # set properties
        # self.setCacheMode(CacheBackground)
        self.setRenderHint(QPainter.Antialiasing)

        # define pens:
        self.pen_pc = QPen()
        self.pen_pc.setWidth(0.0001) # 0.1mm width

        self.pen_pc_selected = QPen()
        self.pen_pc_selected.setWidth(0.0001)
        self.pen_pc_selected.setColor(QColor('red'))

        self.pen_wall = QPen()
        self.pen_wall.setWidthF(0.02)

        self.pen_wall_selected = QPen()
        self.pen_wall_selected.setWidthF(0.02)
        self.pen_wall_selected.setColor(QColor('red'))

        self.pen_path = QPen()
        self.pen_path.setWidthF(0.01)
        self.pen_path.setColor(QColor('blue'))

        self.pen_feeder = QPen()
        self.pen_feeder.setWidthF(0.02)
        self.pen_feeder.setColor(QColor('red'))

        self.pen_start_pos = QPen()
        self.pen_start_pos.setWidthF(0.02)
        self.pen_start_pos.setColor(QColor('green'))



    def add_wall(self, wall):
        x1 = wall.x1()
        y1 = wall.y1()
        x2 = wall.x2()
        y2 = wall.y2()

        g_line = self.scene().addLine(x1 , y1 , x2 , y2 , self.pen_wall)
        g_line.setFlag(QGraphicsItem.ItemIsMovable)

        wall.wall_modified.connect(self.update_wall)
        wall.wall_selected_changed.connect(self.update_wall)
        wall.delete_signal.connect(self.remove_graphics)

        self.graphics[wall] = {'line': g_line}
        self.wall_from_graphics[g_line] = wall
        self.fit_scene_in_view()

    def add_feeder(self, feeder):
        x = feeder.x()
        y = feeder.y()
        r = self.feeder_drawing_radius

        g_point = self.scene().addEllipse(x - r, y - r, 2 * r, 2 * r, self.pen_feeder)
        # g_point.setFlag(QGraphicsItem.ItemIsMovable)

        feeder.signal_modified.connect(self.update_feeder)
        feeder.signal_selected_changed.connect(self.update_feeder)
        feeder.signal_delete.connect(self.remove_graphics)

        self.graphics[feeder] = {'ellipse': g_point}
        self.feeder_from_graphics[g_point] = feeder
        self.fit_scene_in_view()

    def add_start_pos(self, start_pos):
        x = start_pos.x()
        y = start_pos.y()
        r = self.start_pos_drawing_radius

        g_point = self.scene().addEllipse(x - r, y - r, 2 * r, 2 * r, self.pen_start_pos)
        # g_point.setFlag(QGraphicsItem.ItemIsMovable)

        start_pos.signal_modified.connect(self.update_start_pos)
        start_pos.signal_selected_changed.connect(self.update_start_pos)
        start_pos.signal_delete.connect(self.remove_graphics)

        self.graphics[start_pos] = {'ellipse': g_point}
        self.start_pos_from_graphics[g_point] = start_pos
        self.fit_scene_in_view()

    def add_pc(self, pc):
        x = pc.x()
        y = pc.y()
        r = pc.r()
        # print('here!')
        # g_ellipse = DraggableEllipse(x-r, y-r, 2*r, 2*r)
        # print('here2!')
        # self.scene().addItem(g_ellipse)

        g_ellipse = self.scene().addEllipse(x - r, y - r, 2 * r, 2 * r, self.pen_pc)
        g_ellipse.setFlag(QGraphicsItem.ItemIsMovable)

        pc.pc_modified.connect(self.update_pc)
        pc.pc_selected_changed.connect(self.update_pc)
        pc.delete_signal.connect(self.remove_graphics)

        self.graphics[pc] = {'ellipse': g_ellipse}
        self.pc_from_graphic[g_ellipse] = pc
        self.fit_scene_in_view()

    def update_wall(self, wall):
        wall_graphics = self.graphics[wall]
        g_line = wall_graphics['line']
        if wall.is_hidden():
            g_line.hide()
        else:
            pen = self.pen_wall_selected if wall.selected() else self.pen_wall
            g_line.show()
            g_line.setPen(pen)
            g_line.setLine(wall.x1(), wall.y1(), wall.x2(), wall.y2())
        # self.fit_scene_in_view()

    def update_feeder(self, feeder):
        object_graphics = self.graphics[feeder]
        graphic = object_graphics['ellipse']
        if feeder.is_hidden():
            graphic.hide()
        else:
            pen = self.pen_feeder_selected if feeder.selected() else self.pen_feeder
            graphic.show()
            graphic.setPen(pen)
            x = feeder.x()
            y = feeder.y()
            r = self.feeder_drawing_radius
            graphic.setRect(x-r, y-r, 2*r, 2*r)

    def update_start_pos(self, start_pos):
        object_graphics = self.graphics[start_pos]
        graphic = object_graphics['ellipse']
        if start_pos.is_hidden():
            graphic.hide()
        else:
            pen = self.pen_start_pos_selected if start_pos.selected() else self.pen_start_pos
            graphic.show()
            graphic.setPen(pen)
            x = start_pos.x()
            y = start_pos.y()
            r = self.start_pos_drawing_radius
            graphic.setRect(x-r, y-r, 2*r, 2*r)

    def update_pc(self, pc):
        pc_graphics = self.graphics[pc]
        g_ellipse = pc_graphics['ellipse']
        if pc.is_hidden():
            g_ellipse.hide()
        else:
            pen = self.pen_pc_selected if pc.selected() else self.pen_pc
            g_ellipse.show()
            g_ellipse.setPen(pen)
            x = pc.x()
            y = pc.y()
            r = pc.r()
            g_ellipse.setRect(x-r, y-r, 2*r, 2*r)
        # self.fit_scene_in_view()


    def remove_graphics(self, key):
        graphics = self.graphics[key]
        if graphics is not None:
            for g in graphics.items():
                self.scene().removeItem(g[1])
            del self.graphics[key]
            self.fit_scene_in_view()

    def fit_scene_in_view(self, force_fit = False):
        if self.auto_fit or force_fit:
            b = self.scene().itemsBoundingRect()
            if b.width() > 0 and b.height() > 0:
                self.view_rect = b
        self.handle_resize()

    def handle_resize(self):
        w = self.width()
        h = self.height()

        # add a buffer for visualizing borders
        buffer = 0.05
        # calculate min x, max y, width and height of the scene (including buffer)
        rw = self.view_rect.width() * (1 + buffer)
        rh = self.view_rect.height() * (1 + buffer)
        mx = self.view_rect.x() - self.view_rect.width() * buffer/2
        My = self.view_rect.y() + self.view_rect.height() * (1 + buffer/2)

        # calculate scale (keep aspect ratio)
        s = w / rw if rh == 0 else h / rh if rw == 0 else min(w / rw, h / rh)

        # create transform
        t = QTransform()
        t.translate(-mx, -My)
        t.scale(s, -s)
        self.setTransform(t)

    # def keyPressEvent(self, event: QKeyEvent) -> None:
    #     if event.modifiers() & Qt.ControlModifier:
    #         self.setDragMode(QGraphicsView.ScrollHandDrag)
    #         self.setInteractive(False)
    #
    # def keyReleaseEvent(self, event: QKeyEvent) -> None:
    #     if not (event.modifiers() & Qt.ControlModifier):
    #         self.setDragMode(QGraphicsView.NoDrag)
    #         self.setInteractive(True)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() & Qt.ControlModifier:
            s = 1 + event.angleDelta().y() / 120 * 0.1
            self.scale(s, s)
        else:
            is_x_bar = event.angleDelta().x() != 0
            bar = self.horizontalScrollBar() if is_x_bar else self.verticalScrollBar()
            bar.event(event)



    def mousePressEvent(self, event: QMouseEvent) -> None:

        # if control key is not down, clear selection
        if not (QApplication.keyboardModifiers() & Qt.ControlModifier):
            PlaceCell.clear_all_selected()
            Wall.clear_all_selected()

        # check if item selected
        item = self.itemAt(event.x(), event.y())


        if item in self.pc_from_graphic:
            # select pc
            self.dragging_pc = self.pc_from_graphic[item]
            self.dragging_start_pos = self.mapToScene(event.x(), event.y())
            self.dragging_pc.setSelected(True)

        elif item in self.wall_from_graphics:
            self.dragging_wall = self.wall_from_graphics[item]
            self.dragging_start_pos = self.mapToScene(event.x(), event.y())
            self.dragging_wall.setSelected(True)



    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragging_pc is not None:
            scene_pos = self.mapToScene(event.x(), event.y())
            self.dragging_pc.translate(scene_pos - self.dragging_start_pos)
            self.dragging_start_pos = scene_pos
        elif self.dragging_wall is not None:
            scene_pos = self.mapToScene(event.x(), event.y())
            self.dragging_wall.translate(scene_pos - self.dragging_start_pos)
            self.dragging_start_pos = scene_pos


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.dragging_pc = None
        self.dragging_wall = None
        self.dragging_start_pos = None

    def add_paths(self, paths):
        for path in paths:
            graphics = []
            for i in range(1, len(path)):
                start = path[i-1]
                end = path[i]
                g_line = self.scene().addLine(start[0] , start[1], end[0] , end[1] , self.pen_path)
                g_line.setFlag(QGraphicsItem.ItemIsMovable)
                g_line.setZValue(-10)
                graphics += [g_line]

            self.path_graphics += [graphics]

    def clear_paths(self):
        # remove paths:
        for path in self.path_graphics:
            for graphic in path:
                self.scene().removeItem(graphic)
        self.path_graphics = []


