from PySide.QtGui  import *

from programValues import *
from Button        import Button

import sys

class Technicals(QWidget):
    """Houses all the technicals in one class"""

    def __init__(self, parent=None):
        super(Technicals, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.scroll = parent
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)

    def addTechnical(self, parent, params, title):
        tech = Technical(self, params, title)
        self.layout.addWidget(tech)


class Technical(QGroupBox):

    def __init__(self, parent=None, params=None, title="blank"):

        super(Technical, self).__init__(parent)

        title = "%s (%s)" % (title, params["abbr"])
        self.setTitle(title)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.technicals = parent
        layout          = QVBoxLayout(self)
        layout.addLayout(self.setToolLayout(params))
        layout.addWidget(self.setGraph())


    def setGraph(self):
        graph = QGraphicsView()
        graph.setFixedHeight(50)
        return graph

    def setToolLayout(self, params):

        layout = QHBoxLayout()
        layout.addLayout(self.setParameters(params))
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
            layout.addWidget(Button(self, action, objID))
        return layout

    def setParameters(self, params):

        layout = QHBoxLayout()
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
            layout.addWidget(label)
            layout.addWidget(parm)
        return layout


if __name__ == "__main__":
    import test
