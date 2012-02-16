from PySide.QtCore import *
from PySide.QtGui  import *

import sys

TECHNICALS = {
# ---------------------------------------------------------------------------- #
"Tech Name" : {
          "abbr": "accronim",
               0: {
                    "name"    : "One",
                    "class"   : "QLineEdit",
                    "methods" : [["setText", "Hello!"],
                                 ["setFixedWidth", 50],]
                   },
                    
               1: {
                    "name"    : "Two",
                    "class"   : "QPushButton",
                    "methods" : [["setText", "Push Me"],],
                   },
              },
# ---------------------------------------------------------------------------- #
"Another Tech": {
            "abbr": "AT",
                0: {
                    "name"    : "1A",
                    "class"   : "QLineEdit",
                    "methods" : [["setText", "Text for 1A"],],
                    },
                1: {
                    "name"    : "2B",
                    "class"   : "QLineEdit",
                    "methods" : [["setText", "Text for 2b"],],
                    },
                },
# ---------------------------------------------------------------------------- #
    }

class Main(QWidget):
    
    
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        layout = QVBoxLayout(self)
        
        layout.addWidget(QGraphicsView())
        layout.addLayout(self.setTechnicals())
        layout.addWidget(self.setScrollArea())
        
        self.addTechButton.pressed.connect(self.addTechnical)
        
        
    def setScrollArea(self):
        scroll        = QScrollArea(self)
        self.techView = TechnicalView(scroll)
        
        scroll.setWidget(self.techView)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(150)
        return scroll
        
        
    def setTechnicals(self):
        layout             = QHBoxLayout()
        techList           = self.getTechnicals()
        self.comboBox      = QComboBox()
        self.addTechButton = QPushButton("Add Technical")
        
        self.comboBox.addItems(techList)
        
        layout.addWidget(self.comboBox)
        layout.addWidget(self.addTechButton)

        return layout

        
    def getTechnicals(self):
        keys = TECHNICALS.keys()
        keys.sort()
        return keys


    def addTechnical(self):
        name   = self.comboBox.currentText()
        params = TECHNICALS[name]
        self.techView.layout.addWidget(Technical(self.techView, params, name))


class TechnicalView(QWidget):
    
    def __init__(self, parent=None):
        super(TechnicalView, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        

class Technical(QGroupBox):
    
    def __init__(self, parent=None, parameters=None, title="blank"):
        
        super(Technical, self).__init__(parent)
        
        title = "%s (%s)" % (title, parameters["abbr"])
        self.setTitle(str(title))
        
        self.parent = parent
        layout      = QVBoxLayout(self)
        toolLayout  = QHBoxLayout()
    
        toolLayout.addLayout(self.setParameters(parameters))
        toolLayout.addStretch()
        toolLayout.addLayout(self.setActions())
        
        layout.addLayout(toolLayout)
        
    
    def setActions(self):
        actionList = ["go-bottom.png", 
                      "go-down.png",
                      "go-up.png", 
                      "go-top.png",
                      "process-stop.png"]
                      
        layout = QHBoxLayout()
        for action in actionList:
            if action == "process-stop.png":
                layout.addWidget(QLabel("   "))
            layout.addWidget(ActionButton(action, self))
        return layout
    
        
    def setParameters(self, parameters):
                
        layout = QHBoxLayout()
        for key in xrange(len(parameters)-1):
            parm = getattr(sys.modules[__name__], parameters[key]["class"])
            parm = parm()
            
            for method in parameters[key]["methods"]:
                getattr(parm, method[0]).__call__(method[1])
            
            label = QLabel(parameters[key]["name"])
            layout.addWidget(label)
            layout.addWidget(parm)
        return layout


class ActionButton(QLabel):
    
    def __init__(self, image=None, parent=None):
        super(ActionButton, self).__init__(parent)
        self.setPixmap(QPixmap(image))
        self.name   = image
        self.parent = parent

    def mousePressEvent(self, event):
        
        if self.name == "process-stop.png":
            self.parent.setParent(None) # Technical -> None
            self.parent.parent.layout.removeWidget(self.parent)
            
            
            
            
app = QApplication([])
main = Main()
main.show()
sys.exit(app.exec_())
