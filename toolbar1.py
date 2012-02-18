from PySide.QtGui import *

from button       import Button

class Toolbar1(QHBoxLayout):
    """Toolbar at the top of the program"""

    def __init__(self, parent=None):
        super(Toolbar1, self).__init__(None)

        symbol = QLabel("Ticker")
        entry  = QLineEdit()
        search = Button(entry, "search.png", "GetSymbolData")
        
        new    = Button(parent, "new.png", "New")
        open   = Button(parent, "open.png", "Open")
        save   = Button(parent, "save.png", "Save")
        
        pref   = Button(parent, "preferences.png", "Preferences")
        term   = Button(parent, "terminal.png", "Terminal")

        entry.setFixedWidth(75)

        self.addWidget(symbol)
        self.addWidget(entry)
        self.addWidget(search)
        
        self.addStretch()
        
        self.addWidget(new)
        self.addWidget(open)
        self.addWidget(save)
        
        self.addStretch()
        
        self.addWidget(pref)
        self.addWidget(term)

        new.signal.connect(self.new)
        save.signal.connect(self.save)
        open.signal.connect(self.open)
        
    def new(self, kwargs):
        print kwargs
        
    def save(self, kwargs):
        print kwargs
        
    def open(self, kwargs):
        print kwargs
    

if __name__ == "__main__":
    import control
