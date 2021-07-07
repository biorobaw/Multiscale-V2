import sys
import numpy as np
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QDoubleSpinBox


class PlaceCell(QWidget):

    pc_modified = pyqtSignal(object)
    pc_selected_changed = pyqtSignal(object)
    delete_signal = pyqtSignal(object)
    all_selected = set()

    def __init__(self, x, y, r, *args, **kwargs):
        super(PlaceCell, self).__init__(*args, **kwargs)

        self.is_selected = False

        self.widget_show = QCheckBox(self)
        self.widget_x = QDoubleSpinBox(self)
        self.widget_y = QDoubleSpinBox(self)
        self.widget_r = QDoubleSpinBox(self)
        self.widgets = [self.widget_show, self.widget_x, self.widget_y, self.widget_r]

        # init chckbox show
        self.widget_show.setCheckState(Qt.Checked)

        # create editable fields
        for widget in self.widgets[1:]:
            widget.setDecimals(3)
            widget.setMinimum(-10000 if widget != self.widget_r else 0)
            widget.setMaximum(10000)
            widget.setFrame(False)
            widget.setSingleStep(0.01)
            widget.setAlignment(Qt.AlignCenter)

        self.widget_x.setValue(x)
        self.widget_y.setValue(y)
        self.widget_r.setValue(r)

        # connect signals and slots
        self.widget_show.stateChanged.connect(self.pc_changed)
        for widget in self.widgets[1:]:
            widget.valueChanged.connect(self.pc_changed)

    def x(self):
        return self.widget_x.value()

    def y(self):
        return self.widget_y.value()

    def r(self):
        return self.widget_r.value()

    def translate(self, vector):
        self.widget_x.setValue(self.x() + vector.x())
        self.widget_y.setValue(self.y() + vector.y())
        self.pc_changed()

    def setSelected(self, new_val: bool):
        # check if value changed
        if new_val != self.is_selected:

            # add or remove from selected set
            if new_val:
                PlaceCell.all_selected.add(self)
            elif self in PlaceCell.all_selected:
                PlaceCell.all_selected.remove(self)

            # set new value and signal
            self.is_selected = new_val
            self.pc_selected_changed.emit(self)

    def selected(self):
        return self.is_selected

    def is_hidden(self):
        return self.widget_show.checkState() == Qt.Unchecked

    def pc_changed(self):
        self.pc_modified.emit(self)

    @staticmethod
    def clear_all_selected():
        aux = PlaceCell.all_selected
        PlaceCell.all_selected = set()
        for pc in aux:
            pc.setSelected(False)

    def delete(self):
        if self in PlaceCell.all_selected:
            PlaceCell.all_selected.remove(self)
        self.delete_signal.emit(self)

    def __str__(self):
        return f'{self.x():9.3f}, {self.y():9.3f}, {self.r():9.2f}'

    @staticmethod
    def fromstring(s):
        args = np.fromstring(s.replace('[','').replace(']',''), sep=",")
        if len(args) == 3:
            return PlaceCell(args[0], args[1], args[2])
        else:
            print('PC parse error')
            return None

    def pickable(self):
        return PickablePlaceCell(self.x(), self.y(), self.r())

class PickablePlaceCell:

    def __init__(self, x, y, r):
        self.data = [x, y, r]


    def x(self):
        return self.data[0]

    def y(self):
        return self.data[1]

    def r(self):
        return self.data[2]
