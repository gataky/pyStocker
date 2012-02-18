from PySide.QtGui  import *
from programValues import *

from toolbar1      import Toolbar1
from toolbar2      import Toolbar2
from graph         import Graph
from button        import Button
from technicals    import *

import sys
import os

class Control(QWidget):
    """Main program that handles everything"""

    def __init__(self, parent=None):
        super(Control, self).__init__(parent)
        layout = QVBoxLayout(self)

        layout.addLayout(Toolbar1(self))

        self.graph = Graph(self)
        layout.addWidget(self.graph)

        layout.addLayout(Toolbar2(self))

        self.scrollArea = ScrollArea(self)
        layout.addWidget(self.scrollArea)


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

            
            

app  = QApplication([])
main = Control()
main.resize(600, 400)
main.show()
sys.exit(app.exec_())
