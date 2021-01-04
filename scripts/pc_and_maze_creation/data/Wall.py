
import sys
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QCheckBox, QDoubleSpinBox


class Wall(QWidget):

    wall_modified = pyqtSignal(object)

    def __init__(self, x1, y1, x2, y2, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)

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

    def is_hidden(self):
        return self.widget_show.checkState() == Qt.Unchecked

    def modified(self):
        print(self.xml_tag())

    def xml_tag(self):
        return f'<wall x1="{self.x1()}" y1="{self.y1()}" x2="{self.x2()}" y2="{self.y2()}" />'

    def wall_changed(self):
        self.wall_modified.emit(self)