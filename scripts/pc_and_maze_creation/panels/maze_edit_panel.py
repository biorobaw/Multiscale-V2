import sys, os, ast
import importlib.util as loader
from multiprocessing import Pool
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, \
                            QWidget, QVBoxLayout, QTableWidget, \
                            QHeaderView, QCheckBox, QTableWidgetItem, \
                            QItemDelegate, QLineEdit, QDoubleSpinBox, QPushButton, \
                            QSpacerItem, QHBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtGui import QPalette, QColor, QDoubleValidator
from PyQt5.QtCore import Qt, pyqtSignal
import pandas as pd

sys.path.append('../utils')
import MazeParser

from data.Wall import Wall
from data.Feeder import Feeder
from data.StartPos import StartPos
from tools.path_planning.precision_planner import find_path, generate_maze_metrics



class PanelMazeEdit(QWidget):

    wall_added = pyqtSignal(Wall)
    wall_removed = pyqtSignal(Wall)

    feeder_added = pyqtSignal(Feeder)
    feeder_removed = pyqtSignal(Feeder)
    
    start_pos_added = pyqtSignal(StartPos)
    start_pos_removed = pyqtSignal(StartPos) 

    signal_clear_paths = pyqtSignal()
    signal_paths_added = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(PanelMazeEdit, self).__init__(*args, **kwargs)
        self.setMinimumSize(100, 100)
        self.pool = None
        self.maze_metrics = None

        # create data container:
        self.walls = []
        self.feeders = []
        self.start_positions = []
        self.last_file_loaded = 'data_generators/default_maze_generator.py'

        # create the layout for the panel
        layout_pane = QVBoxLayout()
        self.setLayout(layout_pane)

        # create the table to display data
        table_widget = QTableWidget()
        table_widget.setSelectionBehavior(table_widget.SelectRows)
        table_widget.setColumnCount(5)
        table_widget.setHorizontalHeaderLabels(('show', 'x1', 'y1', 'x2', 'y2'))
        table_widget.setRowCount(0)
        header = table_widget.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.Fixed)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget = table_widget
        layout_pane.addWidget(table_widget)

        # add buttons widget
        widget_buttons = QWidget(self)
        # widget_buttons.setContentsMargins(0,0,0,0,)
        layout_pane.addWidget(widget_buttons)
        layout_pane.setContentsMargins(0, 0, 0, 0)
        layout_buttons = QHBoxLayout(self)
        widget_buttons.setLayout(layout_buttons)

        button_less = QPushButton(self)
        button_less.setText("-")
        button_less.setMaximumWidth(20)
        button_less.setDisabled(True)
        button_less.clicked.connect(self.delete_selection)
        self.button_less = button_less

        button_add = QPushButton(self)
        button_add.setText("+")
        button_add.setMaximumWidth(20)
        button_add.clicked.connect(self.add_wall)

        button_load = QPushButton(self)
        button_load.setText("load")
        button_load.setMaximumWidth(60)
        button_load.clicked.connect(self.load)

        button_save = QPushButton(self)
        button_save.setText("save")
        button_save.setMaximumWidth(60)
        button_save.clicked.connect(self.save)

        button_reload = QPushButton(self)
        button_reload.setText("reload")
        button_reload.setMaximumWidth(60)
        button_reload.clicked.connect(self.reload)

        button_clear = QPushButton(self)
        button_clear.setText("clear")
        button_clear.setMaximumWidth(60)
        button_clear.clicked.connect(self.clear)



        layout_buttons.addSpacerItem(QSpacerItem(150, 10, QSizePolicy.Expanding))
        layout_buttons.addWidget(button_less)
        layout_buttons.addWidget(button_add)
        layout_buttons.addWidget(button_save)
        layout_buttons.addWidget(button_load)
        layout_buttons.addWidget(button_reload)
        layout_buttons.addWidget(button_clear)

        table_widget.selectionModel().selectionChanged.connect(self.selection_changed)


    def selection_changed(self, selected, deselected):

        rows = set()
        for i in deselected.indexes():
            r = i.row()
            if r not in rows:
                rows.add(r)
                self.walls[r].setSelected(False)

        for i in selected.indexes():
            r = i.row()
            if r not in rows:
                rows.add(r)
                self.walls[r].setSelected(True)

        # activate / deactivate button less
        selection = self.table_widget.selectionModel()
        self.button_less.setEnabled(selection.hasSelection())

    def select_wall(self, wall):
        if wall in self.walls:
            row = self.walls.index(wall)

            # get index of item in table and selection model
            for col in range(0, self.table_widget.columnCount()):
                index  = self.table_widget.model().index(row, col)
                model = self.table_widget.selectionModel()

                # read current selection value:
                # current_val = model.isSelected(index)
                new_val = model.Select if wall.selected() else model.Deselect

                # observation: it seems using the selection model directly does not generate selection changed events
                # which avoids signal loops
                model.select(index, new_val)

            self.table_widget.scrollTo(self.table_widget.model().index(row, 0))

    def delete_selection(self):
        indexes = [r.row() for r in self.table_widget.selectionModel().selectedRows()]
        self.delete_indexes(indexes)

    def delete_indexes(self, indexes):
        indexes = sorted(indexes)
        for i in range(0, len(indexes)):
            self.table_widget.removeRow(indexes[i] - i)
            wall = self.walls[indexes[i] - i]
            del self.walls[indexes[i] - i]
            wall.delete()

    def clear(self):
        self.delete_indexes(list(range(0, len(self.walls))))
        
        for f in self.feeders:
            f.delete()
        self.feeders = []

        for p in self.start_positions:
            p.delete()
        self.start_positions = []

        self.signal_clear_paths.emit()

    def add_wall(self, x1=0, y1=-1.5, x2=0, y2=1.3, wall_str=""):
        # create wall
        if wall_str != "":
            wall = Wall.fromstring(wall_str)
            if wall is None:
                return
        else:
            wall = Wall(x1, y1, x2, y2, self)
        self.walls += [wall]

        # create row in the table
        row_id = self.table_widget.rowCount()
        self.table_widget.insertRow(row_id)

        fields = ['show', 'x1', 'y1', 'x2', 'y2']
        # add checkbox to table and init value
        cb_widget = QWidget(self.table_widget)
        cb_layout = QVBoxLayout(cb_widget)
        cb_layout.setContentsMargins(0, 0, 0, 0)
        cb_widget.setLayout(cb_layout)

        cb_layout.addWidget(wall.widget_show)
        cb_layout.setAlignment(wall.widget_show, Qt.AlignCenter)

        # add wigets to the table
        self.table_widget.setCellWidget(row_id, 0, cb_widget)
        for i in range(1, len(wall.widgets)):
            self.table_widget.setCellWidget(row_id, i, wall.widgets[i])

        wall.wall_selected_changed.connect(self.select_wall)
        self.wall_added.emit(wall)

    def add_feeder(self, id=1, x=0.5, y=-0.5, feeder_str=""):
        # create feeder
        if feeder_str != "":
            feeder = feeder.fromstring(feeder_str)
            if feeder is None:
                return
        else:
            feeder = Feeder(id, x, y, None)
        
        if feeder not in self.feeders:
            self.feeders += [feeder]
            # feeder.object_changed.connect(self.select_feeder)
            self.feeder_added.emit(feeder)

    def add_start_pos(self, x=0, y=-1.5, w=0, start_pos_str=""):
        # create start_pos
        if start_pos_str != "":
            start_pos = start_pos.fromstring(start_pos_str)
            if start_pos is None:
                return
        else:
            start_pos = StartPos(x, y, w, None)

        if start_pos not in self.start_positions:
            self.start_positions += [start_pos]
            # start_pos.object_changed.connect(self.select_wall)
            self.start_pos_added.emit(start_pos)

    def save(self):
        name = QFileDialog().getSaveFileName(self, 'Save File')[0]
        if name == '':
            return
        if len(name) < 4 or name[-4:] != '.xml':
            name += '.xml'

        num_spaces = 0
        with open(name, 'w') as f:
            f.write('<?xml version="1.0" encoding="us-ascii"?>\n')
            f.write('\n')
            f.write(f'<world>\n')
            f.write('\n')
            for w in self.walls:
                f.write(f'    {w.xml_tag()}\n')
            if len(self.start_positions) > 0:
                f.write('\n')
                f.write('\n')
                f.write('    <startPositions>\n')
                for p in self.start_positions:
                    f.write(f'        {p.xml_tag()}\n')
                f.write('    </startPositions>\n')

            if len(self.feeders) > 0:
                f.write('\n')
                f.write('\n')
                for feeder in self.feeders:
                    f.write(f'    {feeder.xml_tag()}\n')
            f.write('\n')
            f.write('</world>\n')

    def load(self):
        name = QFileDialog().getOpenFileName(self, 'Open File', '', "*.xml; *.py")[0]
        self.load_from_file(name)

    def load_from_file(self, file_name):
        if file_name == '':
            return


        walls, feeders, start_positions = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        try:
            if file_name.endswith(".xml"):
                walls, feeders, start_positions = MazeParser.parse_maze(file_name)
            elif file_name.endswith(".py"):
                spec = loader.spec_from_file_location("maze_loader_file", file_name)
                loader_module = loader.module_from_spec(spec)
                spec.loader.exec_module(loader_module)

                if hasattr(loader_module, 'load_maze_df'):
                    walls, feeders, start_positions = loader_module.load_maze_df()
                else: 
                    print(f'Function "load_maze_df" not implemented in file {file_name}')

                
        except:
            print(f'ERROR: unable to load the file {self.last_file_loaded}')

        try:
            metrics_folder, maze_file_name = os.path.split(file_name)
            metrics_file_name = os.path.join(metrics_folder,'mazeMetrics.csv')
            metrics = pd.read_csv(metrics_file_name)
            metrics = metrics[metrics.maze == maze_file_name].copy().reset_index(drop=True)
            self.maze_metrics = metrics
        except:
            self.maze_metrics = None
            print('Maze metric file not found in maze folder.')
            

        for index, row in walls.iterrows():
            self.add_wall(float(row['x1']), float(row['y1']),
                           float(row['x2']), float(row['y2']))

        for index, row in feeders.iterrows():
            #Currently we only display feeders, we do not allow editting them
            self.add_feeder(int(row['fid']), float(row['x']), float(row['y']))

        for index, row in start_positions.iterrows():
            #Currently we only display feeders, we do not allow editting them
            self.add_start_pos(float(row['x']), float(row['y']), float(row['w']))

        if self.maze_metrics is not None:
            paths = [ast.literal_eval(p) for p in self.maze_metrics.path.values]
            self.signal_paths_added.emit(paths)


        self.last_file_loaded = file_name


    def reload(self):
        self.clear()
        self.load_from_file(self.last_file_loaded)

    
    def process_copy_event(self):
        # get selected walls:
        wall_strs = [ f'[{wall}]' for wall in Wall.all_selected ]
        QApplication.clipboard().setText( '\n'.join( wall_strs) )

    def process_paste_event(self):
        paste_text = QApplication.clipboard().text()
        print(paste_text)
        tokens = paste_text.splitlines()
        for t in tokens:
            self.add_wall(wall_str = t)

    def perform_path_planning(self):
        self.signal_clear_paths.emit()
        i = 0
        paths = []
        pickable_walls = [w.pickable() for w in self.walls]
        args = [ (start.pickable(), goal.pickable(), pickable_walls) for goal in self.feeders for start in self.start_positions]
        args = [ (i,) + a for (i,a) in zip(range(len(args)), args) ]

        if self.pool is None:
            self.pool = Pool(len(args))
            self.pool.starmap_async(find_path, args, chunksize=1, callback = self.path_planning_done)
                # self.path_planning_done(results)
        else:
            print("THREAD POOL ALREADY RUNNING")



    def path_planning_done(self, results):
        # separate and print results
        paths = [ path for (path, distance) in results]
        distances = [ distance for (path, distance) in results ]
        steps = [ len(p)-1 for p in paths]
        print ( *zip(range(len(distances)), steps, distances))
        
        self.pool.terminate()
        self.pool = None

        # signal to the gui
        self.signal_paths_added.emit(paths)
        

    def create_all_maze_metrics(self):
        folder = QFileDialog().getExistingDirectory(self, 'Choose folder with mazes', '')
        if folder is not None and folder != "":
            generate_maze_metrics(folder)

