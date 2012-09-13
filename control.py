from PySide.QtGui  import *
from PySide.QtCore import *
from globals       import *

from utils import Button, Graph, RangeSlider, Technicals, Toolbar1, Toolbar2

import sys
import os


class Control(QWidget):
    """Main program that handles everything"""

    def __init__(self, parent=None):
        super(Control, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.toolbar1   = Toolbar1(self)
        self.graph      = Graph(self)
        self.sliders    = RangeSlider(Qt.Horizontal, self)
        self.toolbar2   = Toolbar2(self)
        self.scrollArea = ScrollArea(self)

        layout.addLayout(self.toolbar1)
        layout.addWidget(self.graph)
        layout.addWidget(self.sliders)
        layout.addLayout(self.toolbar2)
        layout.addWidget(self.scrollArea)

        self.sliders.sliderMoved.connect(self.graph.setSpan)




class ScrollArea(QScrollArea):
    """Where the technicals will show up, appears after ToolBar2"""

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)

        self.control = parent
        self.techs   = Technicals(self)
        self.setWidget(self.techs)
        self.setWidgetResizable(True)

    def addTechnical(self, technicalName):
        self.techs.addTechnical(technicalName)


if __name__ == "__main__":
    import pyStocker

