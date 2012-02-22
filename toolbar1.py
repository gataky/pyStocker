from PySide.QtGui  import *
from PySide.QtCore import *
from button        import Button
from globals       import *

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
        entry  = CLineEdit(self)

        # -------------------------------------------------------------------- # Buttons
        search = Button(entry, "search.png", "GetSymbolData")
        # ---- #
        new    = Button(parent, "new.png", "New")
        open   = Button(parent, "open.png", "Open")
        save   = Button(parent, "save.png", "Save")
        # ---- #
        pref   = Button(parent, "preferences.png", "Preferences")
        term   = Button(parent, "terminal.png", "Terminal")
        help   = Button(parent, "help.png", "Help")

        entry.setFixedWidth(75)

        map(self.addWidget, [symbol, entry, search])
        self.addStretch()
        map(self.addWidget, [new, open, save])
        self.addStretch()
        map(self.addWidget, [pref, term, help])

        # -------------------------------------------------------------------- # Connections
        search.signal.connect(self.getSymbolData)

        new.signal.connect(self.new)
        save.signal.connect(self.save)
        open.signal.connect(self.open)

        pref.signal.connect(self.preferences)
        term.signal.connect(self.terminal)
        help.signal.connect(self.help)


    def getSymbolData(self, lineEdit):
        start  = datetime.date(2010,1,1)
        end    = datetime.date.today()
        ticker = lineEdit.text().upper()

        print "getting symbol data (%s)..." % ticker
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

    def help(self, kwargs):
        print kwargs


class CLineEdit(QLineEdit):

    def __init__(self, parent=None):

        super(CLineEdit, self).__init__(None)
        self.parent = parent

    def keyPressEvent(self, event):

        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            self.parent.getSymbolData(self)
        super(CLineEdit, self).keyPressEvent(event)



if __name__ == "__main__":
    import pyStocker
