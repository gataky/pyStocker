from PySide.QtCore import *
from PySide.QtGui  import *
from programValues import *


import sys


class Main(QWidget):


    def __init__(self, parent=None):

        super(Main, self).__init__(parent)
        layout = QVBoxLayout(self)
        layout.addLayout(self.setToolBar())
        layout.addWidget(QGraphicsView())
        layout.addLayout(self.setTechnicals())
        layout.addWidget(self.setScrollArea())

        self.addTechButton.pressed.connect(self.addTechnical)

    def setScrollArea(self):

        self.scroll   = QScrollArea(self)
        self.techView = TechnicalView(self.scroll)
        self.scroll.setWidget(self.techView)
        self.scroll.setWidgetResizable(True)
        return self.scroll

    def setToolBar(self):

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Ticker"))
        
        self.tickerLine = QLineEdit()
        self.tickerLine.setFixedWidth(50)
        self.tickerLine.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addWidget(self.tickerLine)
        
        symbolSearch = ActionButton("system-search.png", self, "ticker search")
        layout.addWidget(symbolSearch)

        layout.addStretch()
        
        terminal = ActionButton("terminal.png", self, "terminal")
        layout.addWidget(terminal)
        
        return layout

    def setTechnicals(self):

        layout             = QHBoxLayout()
        techList           = self.getTechnicals()
        self.comboBox      = QComboBox()
        self.addTechButton = QPushButton("Add Technical")
        self.techAdjust    = ActionButton("list-remove.png", self, "slider")

        self.comboBox.addItems(techList)

        layout.addWidget(self.comboBox)
        layout.addWidget(self.addTechButton)
        layout.addStretch()
        layout.addWidget(self.techAdjust)
        layout.addStretch()
        return layout

    def getTechnicals(self):
        keys = TECHNICALS.keys()
        keys.sort()
        return keys

    def addTechnical(self):
        name   = self.comboBox.currentText()
        params = TECHNICALS[name]
        self.techView.addTechnical(self.techView, params, name)


class TechnicalView(QWidget):

    def __init__(self, parent=None):
        super(TechnicalView, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)

    def addTechnical(self, parent, parameters, title):
        self.layout.addWidget(self.Technical(parent, parameters, title))


    class Technical(QGroupBox):

        def __init__(self, parent=None, parameters=None, title="blank"):

            super(TechnicalView.Technical, self).__init__(parent)
            
            title = "%s (%s)" % (title, parameters["abbr"])
            self.setTitle(title)
            
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            
            self.parent = parent
            layout      = QVBoxLayout(self)
            layout.addLayout(self.setToolLayout(parameters))

        def setToolLayout(self, parameters):

            layout = QHBoxLayout()
            layout.addLayout(self.setParameters(parameters))
            layout.addStretch()
            layout.addLayout(self.setActions())
            return layout

        def setActions(self):

            actionList = ["go-bottom.png",
                          "go-down.png",
                          "go-up.png",
                          "go-top.png",
                          "process-stop.png"]

            layout = QHBoxLayout()
            for action in actionList:
                if action == "process-stop.png":
                    layout.addWidget(QLabel(" | "))
                objID = action.split(".")[0]
                layout.addWidget(ActionButton(action, self, objID))
            return layout

        def setParameters(self, parameters):

            layout = QHBoxLayout()
            for key in xrange(len(parameters)-1):
                parm = getattr(sys.modules[__name__], parameters[key]["class"])
                parm = parm()

                for method in parameters[key]["methods"]:
                    # method == [class method, [args]]
                    try:
                        # method takes one arg
                        getattr(parm, method[0]).__call__(method[1])
                    except TypeError:
                        # method takes more than one arg thus the "*". This will
                        # unpack method[1] into the method.
                        getattr(parm, method[0]).__call__(*method[1])

                label = QLabel(parameters[key]["name"])
                layout.addWidget(label)
                layout.addWidget(parm)
            return layout


class ActionButton(QLabel):
    """Custom icon buttons made from labels"""

    def __init__(self, image=None, parent=None, objID=None):

        super(ActionButton, self).__init__(parent)
        self.setPixmap(QPixmap(image))
        self.name    = image  # image file name
        self.objID   = objID
        self.parent  = parent
        self.holding = False  # holding the mouse button down?

        self.setMouseTracking(True)

    def mousePressEvent(self, event):

        if self.objID == "process-stop": # delete on a tech
            self.parent.setParent(None) # Technical parent -> None
            self.parent.parent.layout.removeWidget(self.parent)
        
        if self.objID == "slider": # minus button clicked for resizing
            self.holding = True
        
        if self.objID == "ticker search":
            print "getting symbol data"
        
        if self.objID == "terminal":
            print "open python terminal"

    def mouseMoveEvent(self, event):

        if self.holding:
            dy        = event.pos().y()
            height    = self.parent.scroll.geometry().size().height() - dy
            maxHeight = self.parent.size().height() * MAX_HEIGHT_FACTOR
            # don't allow setting too high and can't have negative numbers
            if height >= maxHeight or height <= 0:
                return
            self.parent.scroll.setFixedHeight(height)

    def mouseReleaseEvent(self, event):

        if self.holding:
            self.holding = False


app = QApplication([])
main = Main()
main.show()
sys.exit(app.exec_())
