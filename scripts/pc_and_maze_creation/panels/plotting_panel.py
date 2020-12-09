import sys
from PyQt5.Qt import QApplication, QLabel, QMainWindow, \
                            QWidget, QVBoxLayout, QTableWidget, \
                            QHeaderView, QCheckBox, QTableWidgetItem, \
                            QItemDelegate, QLineEdit, QDoubleSpinBox, QPushButton, \
                            QSpacerItem, QHBoxLayout, QSizePolicy, QFileDialog, \
                            QGraphicsView, QGraphicsScene, QPalette, QColor, \
                            QDoubleValidator, QBrush, QPen, QGraphicsEllipseItem, \
                            QGraphicsRectItem, QGraphicsTextItem, QPen, QLineF, QRectF, Qt, QPainter, QTransform

from .plotting_gview import GViewPlotting

class PanelDataPlotting(QWidget):

    def __init__(self, *args, **kwargs):
        super(PanelDataPlotting, self).__init__(*args, **kwargs)

        # create the layout for the panel
        layout_pane = QVBoxLayout()
        self.setLayout(layout_pane)
        self.setContentsMargins(0, 0, 0, 0)
        layout_pane.setContentsMargins(0, 20, 5, 1)

        # create an empty scene and and a view port
        self.gview = GViewPlotting(self)
        layout_pane.addWidget(self.gview)
