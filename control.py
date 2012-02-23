from PySide.QtGui  import *
from globals       import *

from toolbar1      import Toolbar1
from toolbar2      import Toolbar2
from graph         import *
from button        import Button
from technicals    import *
from sliders       import RangeSlider

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

