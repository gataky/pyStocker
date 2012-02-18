from PySide.QtGui  import *
from programValues import *

import sys
import os

class Control(QWidget):
    """Main program that handles everything"""

    def __init__(self, parent=None):
        super(Control, self).__init__(parent)
        layout = QVBoxLayout(self)

        layout.addLayout(Toolbar1(self))

        self.graphArea = GraphArea(self)
        layout.addWidget(self.graphArea)

        layout.addLayout(Toolbar2(self))

        self.scrollArea = ScrollArea(self)
        layout.addWidget(self.scrollArea)


class Toolbar1(QHBoxLayout):
    """Toolbar at the top of the program"""

    def __init__(self, parent=None):
        super(Toolbar1, self).__init__(None)

        symbol = QLabel("Ticker")
        entry  = QLineEdit()
        search = Button(entry, "search.png", "GetSymbolData")
        term   = Button(parent, "terminal.png", "Terminal")

        entry.setFixedWidth(75)

        self.addWidget(symbol)
        self.addWidget(entry)
        self.addWidget(search)
        self.addStretch()
        self.addWidget(term)


class GraphArea(QGraphicsView):
    """Place holder until we get to putting in matplotlib"""

    def __init__(self, parent=None):
        super(GraphArea, self).__init__(parent)


class Toolbar2(QHBoxLayout):
    """Toolbar for technicals/view adjustment appears after main graph area"""

    def __init__(self, parent=None):
        super(Toolbar2, self).__init__(None)

        label = QLabel("Technicals")
        combo = QComboBox()
        add   = Button(combo, "add.png", "AddTechnical", parent)
        move  = Button(parent, "remove.png", "SlideView")

        combo.addItems(TECHNICALS.keys())

        self.addWidget(label)
        self.addWidget(combo)
        self.addWidget(add)
        self.addStretch()
        self.addWidget(move)
        self.addStretch()


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


class Technicals(QWidget):
    """Widget that houses all technical groupboxes, appears in ScrollArea"""

    def __init__(self, parent=None):
        super(Technicals, self).__init__(parent)
        self.layout = QVBoxLayout()

    def addTechnical(self, technicalName):
        tech = Technical(self, technicalName)
        self.layout.addWidget(tech)


class Technical(QGroupBox):
    """Handles all actions for one technical"""

    def __init__(self, parent=None, technicalName=None):
        super(Technical, self).__init__(parent)

        layout = QVBoxLayout()

        self.setTitle(technicalName)

        layout.addLayout(TechBar(TECHNICALS[technicalName]))
        layout.addWidget(QGraphicsView())


class TechBar(QHBoxLayout):
    """Toolbar that accepts technical parameters and placement buttons"""

    def __init__(self, parameters):
        super(TechBar, self).__init__(None)

        self.setParameters(parameters)

    def setParameters(self, params):

        for key in xrange(len(params)-1):
            parm = getattr(sys.modules[__name__], params[key]["class"])
            parm = parm()

            for method in params[key]["methods"]:
                # method == [class method, [args]]
                try:
                    # method takes one arg
                    getattr(parm, method[0]).__call__(method[1])
                except TypeError:
                    # method takes more than one arg thus the "*". This will
                    # unpack method[1] into the method.
                    getattr(parm, method[0]).__call__(*method[1])

            label = QLabel(params[key]["name"])
            self.addWidget(label)
            self.addWidget(parm)


class Button(QLabel):
    """Custom icon buttons"""

    def __init__(self, parent=None, image=None, id=None, yaya=None):
        super(Button, self).__init__(parent)

        self.image   = os.path.join("imgs", image)
        self.parent  = parent
        self.id      = id
        self.yaya    = yaya  # head of the family i.e. Control
        self.holding = False # is the button being held?

        self.setPixmap(QPixmap(self.image))
        self.setMouseTracking(True)

    def mousePressEvent(self, event):

        if self.id == "GetSymbolData":
            print "get sumbol data"
            print self.id, self.parent
            print self.parent.text()

        if self.id == "Terminal":
            print "open terminal"

        if self.id == "AddTechnical":
            name = self.parent.currentText()
            self.yaya.scrollArea.addTechnical(name)

        if self.id == "SlideView":
            self.holding = True

    def mouseMoveEvent(self, event):

        if self.holding:
            dy        = event.pos().y()
            height    = self.parent.scrollArea.geometry().size().height()
            height   -= dy

            maxHeight = self.parent.size().height() * MAX_HEIGHT_FACTOR
            # don't allow setting too high and can't have negative numbers
            if height >= maxHeight or height <= 0:
                return
            self.parent.scrollArea.setFixedHeight(height)

    def mouseReleaseEvent(self, event):
        self.holding = False


app  = QApplication([])
main = Control()
main.resize(600, 400)
main.show()
sys.exit(app.exec_())
