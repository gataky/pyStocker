from PySide.QtGui import *
from button       import Button
from globals      import *

import matplotlib.finance as finance
import matplotlib.mlab    as mlab
import urllib2
import datetime

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
        start  = datetime.date(2010,1,1)
        end    = datetime.date.today()
        ticker = kwargs["parent"].text().upper()

        print "getting symbol data..."
        for attempt in xrange(GET_DATA_ATTEMPTS):
            try:
                # a numpy record array with fields: 
                #   date, open, high, low, close, volume, adj_close        
                fh    = finance.fetch_historical_yahoo(ticker, start, end)
                data  = mlab.csv2rec(fh)
                fh.close()
                data.sort()
                print "\tsuccess"
                break
            except urllib2.HTTPError:
                print "\tAttempt # %i" % (attempt + 1)
                if attempt == 2:
                    print "\t404 Error: Check ticker/connection"
                    return 
                    
        
        self.control.graph.setData(data)

        
        
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
    import pyStocker
