import sys

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QSplitter, QAction
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
        self.setAcceptDrops(True)

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
        self.pane_plot = pane_plot
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


        self.createMenus()

        # connect signals and slots:
        tab_maze.wall_added.connect(pane_plot.gview.add_wall)
        tab_maze.feeder_added.connect(pane_plot.gview.add_feeder)
        tab_maze.start_pos_added.connect(pane_plot.gview.add_start_pos)
        tab_maze.signal_clear_paths.connect(pane_plot.gview.clear_paths)
        tab_maze.signal_paths_added.connect(pane_plot.gview.add_paths)
        tab_pcs.pc_added.connect(pane_plot.gview.add_pc)

        self.action_do_path_planner.triggered.connect(tab_maze.perform_path_planning)
        self.action_create_maze_metrics.triggered.connect(tab_maze.create_all_maze_metrics)

        self.action_create_layers.triggered.connect(tab_pcs.create_layers)
        self.action_create_layer_metrics.triggered.connect(tab_pcs.create_layer_metrics)


    def load_dafault_data(self):
        self.tab_maze.reload()
        self.tab_pcs.reload()

    def keyReleaseEvent(self, event : QKeyEvent):
        control = event.modifiers() & Qt.ControlModifier

        if control:
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

        if event.key() == Qt.Key_Delete:
            active_widget = self.pane_edit.currentWidget()
            if hasattr(active_widget, 'delete_selection'):
                active_widget.delete_selection()
            else:
                print("widget has no attribute 'delete_selection'")

    def createMenus(self):
        # MENU MAZE
        self.menu_maze = self.menuBar().addMenu('&Maze')

        self.action_do_path_planner = QAction('Do &Path Planning')
        self.action_create_maze_metrics = QAction('Create all &Maze Metrics')

        self.menu_maze.addAction(self.action_do_path_planner)
        self.menu_maze.addAction(self.action_create_maze_metrics)

        # MENU LAYERS 
        self.menu_layers = self.menuBar().addMenu('&Layers')

        self.action_create_layers = QAction('Create &Layers')
        self.action_create_layer_metrics = QAction('Create all Layer &Metrics')

        self.menu_layers.addAction(self.action_create_layers)
        self.menu_layers.addAction(self.action_create_layer_metrics)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]

        control = QApplication.keyboardModifiers() == Qt.ControlModifier
        
        if not control:
            active_tab = self.pane_edit.currentWidget()
            active_tab.clear()

        for f in files:
            self.tab_maze.load_from_file(f)
            self.tab_pcs.load_from_file(f)
            self.pane_plot.gview.fit_scene_in_view(force_fit = True)



        



if __name__ == '__main__':
    app = QApplication(sys.argv)  # start qt
    window = MainWindow()  # create main window
    window.show()          # IMPORTANT!!!!! Windows are hidden by default.
    window.load_dafault_data()
    app.exec_()            # start event loop
