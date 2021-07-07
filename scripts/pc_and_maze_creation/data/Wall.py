
import sys
import numpy as np
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QDoubleSpinBox


class Wall(QWidget):

    wall_modified = pyqtSignal(object)
    wall_selected_changed = pyqtSignal(object)
    delete_signal = pyqtSignal(object)
    all_selected = set()

    def __init__(self, x1, y1, x2, y2, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)

        self.is_selected = False

        self.widget_show = QCheckBox(self)
        self.widget_x1 = QDoubleSpinBox(self)
        self.widget_y1 = QDoubleSpinBox(self)
        self.widget_x2 = QDoubleSpinBox(self)
        self.widget_y2 = QDoubleSpinBox(self)
        self.widgets = [self.widget_show, self.widget_x1, self.widget_y1, self.widget_x2, self.widget_y2]

        # init chckbox show
        self.widget_show.setCheckState(Qt.Checked)

        # create editable fields
        for widget in self.widgets[1:]:
            widget.setDecimals(3)
            widget.setMinimum(-10000)
            widget.setMaximum(10000)
            widget.setFrame(False)
            widget.setSingleStep(0.01)
            widget.setAlignment(Qt.AlignCenter)

        self.widget_x1.setValue(x1)
        self.widget_y1.setValue(y1)
        self.widget_x2.setValue(x2)
        self.widget_y2.setValue(y2)

        # connect signals and slots
        self.widget_show.stateChanged.connect(self.wall_changed)
        for widget in self.widgets[1:]:
            widget.valueChanged.connect(self.wall_changed)

    def x1(self):
        return self.widget_x1.value()

    def y1(self):
        return self.widget_y1.value()

    def x2(self):
        return self.widget_x2.value()

    def y2(self):
        return self.widget_y2.value()

    def translate(self, vector):
        self.widget_x1.setValue(self.x1() + vector.x())
        self.widget_y1.setValue(self.y1() + vector.y())
        self.widget_x2.setValue(self.x2() + vector.x())
        self.widget_y2.setValue(self.y2() + vector.y())
        self.wall_changed()

    def setSelected(self, new_val: bool):
        # check if value changed
        if new_val != self.is_selected:

            # add or remove from selected set
            if new_val:
                Wall.all_selected.add(self)
            elif self in Wall.all_selected:
                Wall.all_selected.remove(self)

            # set new value and signal
            self.is_selected = new_val
            self.wall_selected_changed.emit(self)

    def selected(self):
        return self.is_selected

    def is_hidden(self):
        return self.widget_show.checkState() == Qt.Unchecked

    def wall_changed(self):
        self.wall_modified.emit(self)

    @staticmethod
    def clear_all_selected():
        aux = Wall.all_selected
        Wall.all_selected = set()
        for wall in aux:
            wall.setSelected(False)

    def delete(self):
        if self in Wall.all_selected:
            Wall.all_selected.remove(self)
        self.delete_signal.emit(self)

    def xml_tag(self):
        return f'<wall x1="{self.x1()}" y1="{self.y1()}" x2="{self.x2()}" y2="{self.y2()}" />'

    def __str__(self):
        return f'{self.x1():9.3f}, {self.y1():9.3f}, {self.x2():9.3f}, {self.y2():9.3f},'

    @staticmethod
    def fromstring(s):
        args = np.fromstring(s.replace('[','').replace(']',''), sep=",")
        if len(args) == 4:
            return Wall(args[0], args[1], args[2], args[3])
        else:
            print('Wall parse error')
            return None

    def pickable(self):
        return PickableWall(self.x1(), self.y1(), self.x2(), self.y2())

class PickableWall:

    def __init__(self, x1, y1, x2, y2):
        self.data = [x1, y1, x2, y2]

    def x1(self):
        return self.data[0]

    def y1(self):
        return self.data[1]

    def x2(self):
        return self.data[2]

    def y2(self):
        return self.data[3]
