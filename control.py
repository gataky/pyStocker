#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

if __name__ == "__main__":
    import pyStocker

from PySide.QtGui  import *
from PySide.QtCore import *
from globals       import *

from utils import Button, Graph, RangeSlider, Technicals, Toolbar1, Toolbar2, QIPythonWidget, DateRange

import sys
import os


class Control(QWidget):
    """Main program that handles everything"""

    def __init__(self, parent=None):
        super(Control, self).__init__(parent)

        self.exit            = False
        self.terminalVisible = True

        layout1 = QHBoxLayout(self)  # Top master layout
        layout2 = QVBoxLayout(self)  # widget on the left
        layout3 = QVBoxLayout(self)  # terminal on the right

        self.toolbar1   = Toolbar1(self)
        self.graph      = Graph(self)
        self.dateRange  = DateRange(self)
        self.sliders    = RangeSlider(Qt.Horizontal, self)
        self.toolbar2   = Toolbar2(self)
        self.scrollArea = ScrollArea(self)
        self.terminal   = QIPythonWidget(parent=self, namespace={"Control":self}, visible=self.terminalVisible)

        layout2.addLayout(self.toolbar1)
        layout2.addWidget(self.graph)
        layout2.addLayout(self.dateRange)
        layout2.addWidget(self.sliders)
        layout2.addLayout(self.toolbar2)
        layout2.addWidget(self.scrollArea)

        layout3.addWidget(self.terminal)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        self.sliders.sliderMoved.connect(self.graph.setSpan)

        QShortcut(QKeySequence("Ctrl+I"), self, self.showTerminal)

    def showTerminal(self):
        self.toolbar1.terminal(None)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            if self.exit:
                sys.exit()
            else:
                self.exit = True


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
