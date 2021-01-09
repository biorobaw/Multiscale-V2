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

class GViewPlotting(QGraphicsView):

    graphics = {}  # hash to store graphic elements
    pc_from_graphic = {}
    view_rect = QRectF(-1, -1, 2, 2)  # user defined rectangle of scene coordinates
    auto_fit = True



    def __init__(self, *args, **kwargs):
        super(GViewPlotting, self).__init__(*args, **kwargs)

        self.dragging_pc = None
        self.dragging_start_pos = None

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


    def add_wall(self, wall):
        p = QPen()
        p.setWidth(0.001)  # 1mm width
        g_line = self.scene().addLine(wall.x1(), wall.y1(), wall.x2(), wall.y2(), p)
        wall.wall_modified.connect(self.update_wall)
        self.graphics[wall] = {'line': g_line}
        self.fit_scene_in_view()

    def update_wall(self, wall):
        wall_graphics = self.graphics[wall]
        g_line = wall_graphics['line']
        if wall.is_hidden():
            g_line.hide()
        else:
            g_line.show()
            g_line.setLine(wall.x1(), wall.y1(), wall.x2(), wall.y2())
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

    def fit_scene_in_view(self):
        if self.auto_fit:
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
            if event.angleDelta().x() != 0:
                self.horizontalScrollBar().wheelEvent(event)
            else:
                self.verticalScrollBar().wheelEvent(event)



    def mousePressEvent(self, event: QMouseEvent) -> None:

        # if control key is not down, clear selection
        if not (QApplication.keyboardModifiers() & Qt.ControlModifier):
            PlaceCell.clear_all_selected()

        # check if item selected
        item = self.itemAt(event.x(), event.y())

        if item in self.pc_from_graphic:
            # select pc
            self.dragging_pc = self.pc_from_graphic[item]
            self.dragging_start_pos = self.mapToScene(event.x(), event.y())
            self.dragging_pc.setSelected(True)



    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragging_pc is not None:
            scene_pos = self.mapToScene(event.x(), event.y())
            self.dragging_pc.translate(scene_pos - self.dragging_start_pos)
            self.dragging_start_pos = scene_pos


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.dragging_pc = None
        self.dragging_start_pos = None



