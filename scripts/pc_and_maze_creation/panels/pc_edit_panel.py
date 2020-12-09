import sys
import importlib.util as loader

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, \
                            QWidget, QVBoxLayout, QTableWidget, \
                            QHeaderView, QCheckBox, QTableWidgetItem, \
                            QItemDelegate, QLineEdit, QDoubleSpinBox, QPushButton, \
                            QSpacerItem, QHBoxLayout, QSizePolicy, QFileDialog
from PyQt5.QtGui import QPalette, QColor, QDoubleValidator
from PyQt5.QtCore import Qt, pyqtSignal
import pandas as pd

from data.PC import PlaceCell

class PanelPCEdit(QWidget):

    pc_added = pyqtSignal(PlaceCell)
    pc_removed = pyqtSignal(PlaceCell)

    def __init__(self, *args, **kwargs):
        super(PanelPCEdit, self).__init__(*args, **kwargs)
        self.setMinimumSize(100, 100)

        # create data container:
        self.pcs = []
        self.last_file_loaded = "default_cell_generator.py"

        # create the layout for the panel
        layout_pane = QVBoxLayout()
        self.setLayout(layout_pane)

        # create the table to display data
        table_widget = QTableWidget()
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(('show', 'x', 'y', 'r'))
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
        button_add.clicked.connect(self.add_entry)

        button_save = QPushButton(self)
        button_save.setText("save")
        button_save.setMaximumWidth(60)
        button_save.clicked.connect(self.save)

        button_load = QPushButton(self)
        button_load.setText("load")
        button_load.setMaximumWidth(60)
        button_load.clicked.connect(self.load)

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

    def selection_changed(self, val1, val2):
        selection = self.table_widget.selectionModel()
        enabled = selection.hasSelection() and len(selection.selectedRows()) > 0
        self.button_less.setEnabled(enabled)

    def delete_selection(self):
        indexes = [r.row() for r in self.table_widget.selectionModel().selectedRows()]
        self.delete_indexes(indexes)

    def delete_indexes(self, indexes):
        for i in range(0, len(indexes)):
            self.table_widget.removeRow(indexes[i]-i)
            pc = self.pcs[indexes[i] - i]
            self.pc_removed.emit(pc)
            del self.pcs[indexes[i]-i]

    def clear(self):
        self.delete_indexes(list(range(0, len(self.pcs))))

    def add_entry(self, x=0, y=0, r=0.08):
        # create place cell
        pc = PlaceCell(x, y, r)
        self.pcs += [pc]

        # create row in the table
        row_id = self.table_widget.rowCount()
        self.table_widget.insertRow(row_id)

        fields = ['show', 'x', 'y', 'r']
        # add checkbox to table and init value
        cb_widget = QWidget(self.table_widget)
        cb_layout = QVBoxLayout(cb_widget)
        cb_layout.setContentsMargins(0, 0, 0, 0)
        cb_widget.setLayout(cb_layout)

        cb_layout.addWidget(pc.widget_show)
        cb_layout.setAlignment(pc.widget_show, Qt.AlignCenter)

        # add wigets to the table
        self.table_widget.setCellWidget(row_id, 0, cb_widget)
        for i in range(1, len(pc.widgets)):
            self.table_widget.setCellWidget(row_id, i, pc.widgets[i])
        self.pc_added.emit(pc)

    def save(self):
        name = QFileDialog().getSaveFileName(self, 'Save File')[0]
        if name == '':
            return
        if len(name) <4 or name[-4:] != '.csv':
            name += '.csv'
        data = [[p.x(), p.y(), p.r()] for p in self.pcs if p.r() > 0]
        df = pd.DataFrame(data, columns=['x', 'y', 'r'])
        df.to_csv(name, index=False)

    def load(self):
        name = QFileDialog().getOpenFileName(self, 'Open File', filter="*.csv;*.py")[0]
        self.load_from_file(name)

    def load_from_file(self, file_name):
        if file_name == '':
            return

        df = pd.DataFrame()
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_name, sep=',')
        elif file_name.endswith(".py"):
            try:
                spec = loader.spec_from_file_location("pc_loader_file", file_name)
                loader_module = loader.module_from_spec(spec)
                spec.loader.exec_module(loader_module)
                df = loader_module.load_pc_df()
                self.last_file_loaded = file_name

            except:
                print("ERROR: the python script couldnt be loaded, check syntax errors in the script")

        for index, row in df.iterrows():
            self.add_entry(float(row['x']), float(row['y']), float(row['r']))

    def reload(self):
        self.clear()
        self.load_from_file(self.last_file_loaded)





