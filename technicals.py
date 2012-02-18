from PySide.QtGui  import *
from programValues import *
from button        import *

import sys

class Technicals(QWidget):
    """Widget that houses all technical groupboxes, appears in ScrollArea"""

    def __init__(self, parent=None):
        super(Technicals, self).__init__(parent)
        self.techLayout = QVBoxLayout(self)
                
        # don't allow added widgets to expand in size
        self.techLayout.setSizeConstraint(QLayout.SetMaximumSize)

    def addTechnical(self, technicalName):
        self.techLayout.addWidget(Technical(self, technicalName))


class Technical(QGroupBox):
    """Handles all actions for one technical"""

    def __init__(self, parent=None, technicalName=None):
        super(Technical, self).__init__(parent)

        self.technicals = parent
        self.setTitle(technicalName)
        
        # Expand on H compress on V
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        layout = QVBoxLayout(self)
        layout.addLayout(TechBar(self, TECHNICALS[technicalName]))
        
        graph = QGraphicsView()
        graph.setFixedHeight(25)
        layout.addWidget(graph)
        

class TechBar(QHBoxLayout):
    """Toolbar that accepts technical parameters and placement buttons"""

    def __init__(self, parent=None, parameters=None):
        super(TechBar, self).__init__(None)

        self.technical = parent
        self.setParameters(parameters)
        self.setButtons()

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

            self.addWidget(QLabel(params[key]["name"]))
            self.addWidget(parm)
            
        self.addWidget(Button(self.technical, "refresh.png", "UpdateTech"))
        self.addStretch()

    def setButtons(self):
        buttons = ["bottom.png",
                   "down.png",
                   "up.png",
                   "top.png",
                   "stop.png"]

        for action in buttons:
            if action == "stop.png":
                self.addWidget(QLabel(" | "))
            objID = action.split(".")[0].capitalize()
            self.addWidget(Button(self.technical, action, objID))


if __name__ == "__main__":
    import control
