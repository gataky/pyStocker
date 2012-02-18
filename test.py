
from PySide.QtGui  import *

from programValues import *
from Technicals    import Technicals
from Button        import Button

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

        self.scroll = QScrollArea(self)
        self.techs  = Technicals(self.scroll)
        self.scroll.setWidget(self.techs)
        self.scroll.setWidgetResizable(True)
        return self.scroll

    def setToolBar(self):

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Ticker"))

        self.tickerLine = QLineEdit()
        self.tickerLine.setFixedWidth(50)
        self.tickerLine.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addWidget(self.tickerLine)

        symbolSearch = Button(self, "system-search.png", "ticker search")
        layout.addWidget(symbolSearch)

        layout.addStretch()

        terminal = Button(self, "terminal.png", "terminal")
        layout.addWidget(terminal)

        return layout

    def setTechnicals(self):

        layout             = QHBoxLayout()
        techList           = self.getTechnicals()
        self.comboBox      = QComboBox()
        self.addTechButton = QPushButton("Add Technical")
        self.techAdjust    = Button(self, "list-remove.png", "slider")

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
        self.techs.addTechnical(self.techs, params, name)



app = QApplication([])
main = Main()
main.resize(600, 400)
main.show()
sys.exit(app.exec_())
