
import sys
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QDoubleSpinBox


class PlaceCell(QWidget):

    pc_modified = pyqtSignal(object)

    def __init__(self, x, y, r, *args, **kwargs):
        super(PlaceCell, self).__init__(*args, **kwargs)

        self.widget_show = QCheckBox(self)
        self.widget_x = QDoubleSpinBox(self)
        self.widget_y = QDoubleSpinBox(self)
        self.widget_r = QDoubleSpinBox(self)
        self.widgets = [self.widget_show, self.widget_x, self.widget_y, self.widget_r]

        # init chckbox show
        self.widget_show.setCheckState(Qt.Checked)

        # create editable fields
        for widget in self.widgets[1:]:
            widget.setDecimals(4)
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

    def is_hidden(self):
        return self.widget_show.checkState() == Qt.Unchecked

    def pc_changed(self):
        self.pc_modified.emit(self)