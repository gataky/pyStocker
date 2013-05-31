from PySide.QtCore import *
from PySide.QtGui  import *

import sys
import numpy as np
import pandas

from talib.abstract import *

data = {
    'open': np.random.random(100),
    'high': np.random.random(100),
    'low': np.random.random(100),
    'close': np.random.random(100),
    'volume': np.random.random(100)}

data = pandas.DataFrame(data)

data = {k: np.array(data[k]) for k in data.columns}



class Tech(QGroupBox):

    def __init__(self, abstractFunction):
        super(Tech, self).__init__()
        self.layout   = QHBoxLayout(self)
        self.function = abstractFunction

        self.setParameters(self.function.input_names.items())
        self.layout.addStretch()

        self.setParameters(self.function.parameters.items())
        self.layout.addStretch()

        self.setTitle()

    def setTitle(self):
        formal = self.function.info["display_name"]
        code   = self.function.info["name"]
        title  = "{} ({})".format(formal, code)
        super(Tech, self).setTitle(title)

    def setParameters(self, parameters):
        groups = QHBoxLayout()
        groups.setSizeConstraint(QLayout.SetFixedSize)

        for parameter, default in parameters:
            if isinstance(default, list):
                groups.addLayout(self.setListParameters(parameter, default))
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

        self.layout.addLayout(groups)

    def setListParameters(self, parameter, default):
        label = QLabel(parameter)
        label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        group = QHBoxLayout()
        group.addWidget(label)

        for item in default:
            widget = QLineEdit()
            widget.setFixedWidth(50)
            widget.setPlaceholderText(item)
            group.addWidget(widget)

        return group



app = QApplication([])
main = Tech(ULTOSC)
main.show()
sys.exit(app.exec_())
