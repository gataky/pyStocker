from PySide.QtGui import *

from button       import Button

class Toolbar1(QHBoxLayout):
    """Toolbar at the top of the program"""

    def __init__(self, parent=None):
        super(Toolbar1, self).__init__(None)

        symbol = QLabel("Ticker")
        entry  = QLineEdit()
        search = Button(entry, "search.png", "GetSymbolData")
        pref   = Button(parent, "preferences.png", "Preferences")
        term   = Button(parent, "terminal.png", "Terminal")

        entry.setFixedWidth(75)

        self.addWidget(symbol)
        self.addWidget(entry)
        self.addWidget(search)
        self.addStretch()
        self.addWidget(pref)
        self.addWidget(term)


if __name__ == "__main__":
    import control
