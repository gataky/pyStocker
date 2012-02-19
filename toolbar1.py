from PySide.QtGui import *

from button       import Button

class Toolbar1(QHBoxLayout):
    """Toolbar at the top of the program"""

    def __init__(self, parent=None):
        super(Toolbar1, self).__init__(None)

        self.control = parent

        symbol = QLabel("Ticker")
        entry  = QLineEdit()
        search = Button(entry, "search.png", "GetSymbolData")
        
        new    = Button(parent, "new.png", "New")
        open   = Button(parent, "open.png", "Open")
        save   = Button(parent, "save.png", "Save")
        
        pref   = Button(parent, "preferences.png", "Preferences")
        term   = Button(parent, "terminal.png", "Terminal")

        entry.setFixedWidth(75)

        map(self.addWidget, [symbol, entry, search])
        self.addStretch()
        map(self.addWidget, [new, open, save])
        self.addStretch()
        map(self.addWidget, [pref, term])

        search.signal.connect(self.getSymbolData)

        new.signal.connect(self.new)
        save.signal.connect(self.save)
        open.signal.connect(self.open)

        pref.signal.connect(self.preferences)
        term.signal.connect(self.terminal)

    def getSymbolData(self, kwargs):
        print kwargs
        
    def new(self, kwargs):
        print kwargs
        
    def save(self, kwargs):
        print kwargs
        
    def open(self, kwargs):
        print kwargs
    
    def preferences(self, kwargs):
        print kwargs

    def terminal(self, kwargs):
        print kwargs

        
if __name__ == "__main__":
    import control
