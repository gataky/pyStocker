from PySide.QtGui  import *
from globals       import *
from button        import *

import sys

class Technicals(QWidget):
    """Widget that houses all technical groupboxes, appears in ScrollArea"""

    def __init__(self, parent=None):
        super(Technicals, self).__init__(parent)
        self.layout  = QVBoxLayout(self)
        self.widgets = []
        # don't allow added widgets to expand in size
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)

    def addTechnical(self, technicalName):
        tech = Technical(self, technicalName)
        self.layout.addWidget(tech)
        self.widgets.append(tech)


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

        btns = ["bottom.png",
                "down.png",
                "up.png",
                "top.png",
                "stop.png"]

        bottom = Button(parent, btns[0], btns[0].split(".")[0].capitalize())
        down   = Button(parent, btns[1], btns[1].split(".")[0].capitalize())
        up     = Button(parent, btns[2], btns[2].split(".")[0].capitalize())
        top    = Button(parent, btns[3], btns[3].split(".")[0].capitalize())
        stop   = Button(parent, btns[4], btns[4].split(".")[0].capitalize())

        map(self.addWidget, [bottom, down, up, top, stop])
        buttonList = [bottom, down, up, top, stop]
        map(lambda x: x.signal.connect(self.handle), buttonList)

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

        update = Button(self.technical, "refresh.png", "UpdateTech")
        update.signal.connect(self.updateTechnical)
        
        self.addWidget(update)
        self.addStretch()

    def handle(self, kwargs):

        parent  = kwargs["parent"]
        id      = kwargs["id"]
        if id == "Stop":
            self.removeTechnical(parent, id)
        else:
            self.moveTechnicals(parent, id)

    def updateTechnical(self, kwargs):
        print kwargs

    def moveTechnicals(self, parent, id):
        
        widgets = parent.technicals.widgets
        index   = widgets.index(parent)
        
        if   id == "Up" and index <> 0:
            newIndex = index - 1
        elif id == "Down" and index <> len(widgets) - 1:
            newIndex = index + 1
        elif id == "Top" and index <> 0:
            newIndex = 0
        elif id == "Bottom" and index <> len(widgets) - 1 :
            newIndex = len(widgets)
        else:
            return
        
        map(parent.technicals.layout.removeWidget, widgets)
        widgets.insert(newIndex, widgets.pop(index))
        map(parent.technicals.layout.addWidget, widgets)

    def removeTechnical(self, parent, id):
        
        parent.technicals.layout.removeWidget(parent)
        parent.setParent(None)
        parent.technicals.widgets.remove(parent)    


if __name__ == "__main__":
    import pyStocker
