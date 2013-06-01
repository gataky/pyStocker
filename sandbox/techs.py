from PySide.QtCore import *
from PySide.QtGui  import *

from collections import OrderedDict
import sys
import numpy as np
import pandas
import os

from talib.abstract import *

data = {
    'open'  : np.random.random(100),
    'high'  : np.random.random(100),
    'low'   : np.random.random(100),
    'close' : np.random.random(100),
    'volume': np.random.random(100)}

data = pandas.DataFrame(data)

data = {k: np.array(data[k]) for k in data.columns}

class Button(QLabel):
    """---- ---- ---- ---- Custom Icon Button
    Button made from a QLabel where we use an image insted of text. Image is
    the name of the file to be used as the image (stord in the imgs dir), ID
    is the "action" (one word discription) of what the button does.  ID is used
    elsewhere for action control ***should replace with objectName***.
    Moveable is if the button is "moveable" meaning this is a sliding button,
    the button itself will not move but mouseTracking is set to True. This
    option is used for sliding resize widget bars.
    """

    clicked = Signal(list)

    def __init__(self, parent=None, image=None, id=None, moveable=False,
                                                                tooltip=None):
        super(Button, self).__init__(parent)

        self.image = os.path.join("../imgs", image)
        self.setPixmap(QPixmap(self.image))

        self.parent   = parent
        self.id       = id
        self.holding  = False # is the button being held?
        self.moveable = moveable

        self.setToolTip(tooltip)

        if moveable:
            self.setMouseTracking(True)

    def mousePressEvent(self, event):

        kwargs = {"id"    : self.id,
                  "parent": self.parent,
                  "pos"   : event.pos()}
        #~ Connected:
        #~ Emits to :
        self.clicked.emit(kwargs)
        self.holding = True

    def mouseMoveEvent(self, event):

        if self.holding and self.moveable:
            kwargs = {"id"    : self.id,
                      "parent": self.parent,
                      "pos"   : event.pos()}
            #~ Connected:
            #~ Emits to :
            self.clicked.emit(kwargs)

    def mouseReleaseEvent(self, event):
        self.holding = False


class TechBar(QHBoxLayout):

    def __init__(self, parent, abstractFunction):
        super(TechBar, self).__init__()
        self.technical  = parent
        self.layout     = QHBoxLayout(self)
        self.function   = abstractFunction
        self.inputs     = OrderedDict()
        self.parameters = OrderedDict()

        self.setParameters(self.function.input_names.items(), "inputs")
        self.layout.addStretch()

        self.setParameters(self.function.parameters.items(), "parameters")
        self.layout.addStretch()

        self.setNavigationButtons()

    def setNavigationButtons(self):
        group = QHBoxLayout()
        for button in ["bottom", "down", "up", "top", "stop"]:
            image = button + ".png"
            buttonObj = Button(self, image, button.capitalize())
                               #~ tooltip=tooltips.get(button))
            group.addWidget(buttonObj)
            buttonObj.clicked.connect(self.handle)
        self.layout.addLayout(group)

    #~ def setTitle(self):
        #~ formal = self.function.info["display_name"]
        #~ code   = self.function.info["name"]
        #~ title  = "{} ({})".format(formal, code)
        #~ super(Tech, self).setTitle(title)

    def setParameters(self, parameters, param_type):
        groups = QHBoxLayout()
        groups.setSizeConstraint(QLayout.SetFixedSize)

        for parameter, default in parameters:
            if isinstance(default, list):
                layout = self.setListParameters(parameter, default, param_type)
                groups.addLayout(layout)
            else:
                widget = QLineEdit()
                widget.setFixedWidth(50)
                widget.setPlaceholderText(str(default))
                label = QLabel(parameter)
                label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                group = QHBoxLayout()
                group.addWidget(label)
                group.addWidget(widget)
                groups.addLayout(group)

            if param_type == "inputs":
                self.inputs[parameter] = default
            elif param_type == "parameters":
                self.parameters[parameter] = default

        self.layout.addLayout(groups)

    def setListParameters(self, parameter, default, param_type):
        label = QLabel(parameter)
        label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        group = QHBoxLayout()
        group.addWidget(label)

        if param_type == "inputs":
            self.inputs[parameter] = default
        elif param_type == "parameters":
            self.parameters[parameter] = default

        for item in default:
            widget = QLineEdit()
            widget.setFixedWidth(50)
            widget.setPlaceholderText(item)
            group.addWidget(widget)

        return group

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


app = QApplication([])
main = Tech(ULTOSC)
main.show()
print main.inputs
print main.parameters

sys.exit(app.exec_())
