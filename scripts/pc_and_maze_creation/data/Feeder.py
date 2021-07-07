import sys
import numpy as np
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QDoubleSpinBox, QSpinBox


class Feeder(QWidget):

    signal_modified = pyqtSignal(object)
    signal_selected_changed = pyqtSignal(object)
    signal_delete = pyqtSignal(object)
    all_selected = set()

    def __init__(self, id, x, y, *args, **kwargs):
        super(Feeder, self).__init__(*args, **kwargs)

        self.is_selected = False

        self.widget_show = QCheckBox(self)
        self.widget_id = QSpinBox(self)
        self.widget_x = QDoubleSpinBox(self)
        self.widget_y = QDoubleSpinBox(self)
        self.widgets = [self.widget_show, self.widget_id, self.widget_x, self.widget_y]

        # init chckbox show
        self.widget_show.setCheckState(Qt.Checked)

        # create editable fields
        for widget in self.widgets[1:]:
            if widget != self.widget_id:
                widget.setDecimals(3)
            widget.setMinimum(-10000)
            widget.setMaximum(10000)
            widget.setFrame(False)
            widget.setSingleStep(0.01 if widget != self.widget_id else 1)
            widget.setAlignment(Qt.AlignCenter)

        self.widget_id.setValue(id)
        self.widget_x.setValue(x)
        self.widget_y.setValue(y)

        # connect signals and slots
        self.widget_show.stateChanged.connect(self.object_changed)
        for widget in self.widgets[1:]:
            widget.valueChanged.connect(self.object_changed)

    def x(self):
        return self.widget_x.value()

    def y(self):
        return self.widget_y.value()

    def id(self):
        return self.widget_id.value()

    def translate(self, vector):
        self.widget_x.setValue(self.x() + vector.x())
        self.widget_y.setValue(self.y() + vector.y())
        self.object_changed()

    def setSelected(self, new_val: bool):
        # check if value changed
        if new_val != self.is_selected:

            # add or remove from selected set
            if new_val:
                Feeder.all_selected.add(self)
            elif self in Feeder.all_selected:
                Feeder.all_selected.remove(self)

            # set new value and signal
            self.is_selected = new_val
            self.signal_selected_changed.emit(self)

    def selected(self):
        return self.is_selected

    def is_hidden(self):
        return self.widget_show.checkState() == Qt.Unchecked

    def object_changed(self):
        self.signal_modified.emit(self)

    @staticmethod
    def clear_all_selected():
        aux = Feeder.all_selected
        Feeder.all_selected = set()
        for pc in aux:
            pc.setSelected(False)

    def delete(self):
        if self in Feeder.all_selected:
            Feeder.all_selected.remove(self)
        self.signal_delete.emit(self)

    def xml_tag(self):
        return f'<feeder id="{self.id()}" x="{self.x()}" y="{self.y()}" />'

    def __str__(self):
        return f'{self.id()}, {self.x():9.3f}, {self.y():9.3f}'

    @staticmethod
    def fromstring(s):
        args = np.fromstring(s.replace('[','').replace(']',''), sep=",")
        if len(args) == 3:
            return Feeder(args[0], args[1], args[2])
        else:
            print('PC parse error')
            return None

    def pickable(self):
        return PickableFeeder(self.id(), self.x(), self.y())   

    def __eq__(self, f2):
        return abs(self.x() - f2.x()) < 0.001 and abs(self.y() - f2.y()) < 0.001

    __hash__ = QWidget.__hash__

class PickableFeeder:

    def __init__(self, id,  x, y):
        self.data = [x, y, id]


    def x(self):
        return self.data[0]

    def y(self):
        return self.data[1]

    def id(self):
        return self.data[2]
