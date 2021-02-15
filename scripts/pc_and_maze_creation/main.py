import sys

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QSplitter
from PyQt5.QtGui import QPalette, QColor, QKeyEvent
from PyQt5.QtCore import Qt

from panels.pc_edit_panel import PanelPCEdit
from panels.maze_edit_panel import PanelMazeEdit
from panels.plotting_panel import PanelDataPlotting
#import pc_edit_panel, maze_edit_panel, plotting_panel


class MainWindow(QMainWindow):
    """ Subclass QMainWindow to customise your application's main window """

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Maze and pc editor")

        # add main widget and create its layout
        widget_main = QWidget()
        self.setCentralWidget(widget_main)
        # layout = QHBoxLayout()
        # widget_main.setLayout(layout)

        # create splitter widget to hold edit and view panes
        splitter = QSplitter(Qt.Horizontal)
        # splitter.setSizes([600, 600])
        # layout.addWidget(splitter)
        pane_edit = QTabWidget()
        pane_plot = PanelDataPlotting()
        splitter.addWidget(pane_edit)
        splitter.addWidget(pane_plot)
        splitter.setStretchFactor(1, 1)

        # create and add tab widget for pc and maze editting
        self.tab_pcs = tab_pcs = PanelPCEdit()
        self.tab_maze = tab_maze = PanelMazeEdit()
        pane_edit.addTab(tab_pcs, "PCs")
        pane_edit.addTab(tab_maze, "maze")
        self.pane_edit = pane_edit

        # create and set main widget's layout
        self.setCentralWidget(splitter)

        self.setMinimumSize(800, 450)

        # connect signals and slots:
        tab_maze.wall_added.connect(pane_plot.gview.add_wall)
        tab_maze.wall_removed.connect(pane_plot.gview.remove_graphics)

        tab_pcs.pc_added.connect(pane_plot.gview.add_pc)


    def load_dafault_data(self):
        self.tab_maze.reload()
        self.tab_pcs.reload()

    def keyReleaseEvent(self, event : QKeyEvent):
        if event.key() == Qt.Key_C:
            active_widget = self.pane_edit.currentWidget()
            if hasattr(active_widget, 'process_copy_event'):
                active_widget.process_copy_event()
            else:
                print("widget has no attribute 'process_copy_event'")

        if event.key() == Qt.Key_V:
            active_widget = self.pane_edit.currentWidget()
            if hasattr(active_widget, 'process_paste_event'):
                active_widget.process_paste_event()
            else:
                print("widget has no attribute 'process_paste_event'")




if __name__ == '__main__':
    app = QApplication(sys.argv)  # start qt
    window = MainWindow()  # create main window
    window.show()          # IMPORTANT!!!!! Windows are hidden by default.
    window.load_dafault_data()
    app.exec_()            # start event loop
