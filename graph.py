if __name__ == "__main__":
    import pyStocker
    import sys
    sys.exit()

from PySide.QtGui import *
from numpy        import arange, sin, pi, zeros_like, diff

import os

#os.environ['QT_API'] = 'pyside'
import matplotlib 
#matplotlib.use('Qt4Agg') # must be called before .backends or .pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure



class Graph(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=4, dpi=70):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        figure = Figure(figsize=(width, height), dpi=dpi)        
        super(Graph, self).__init__(figure)
    
        self.ax = figure.add_subplot(111)
        self.ax.axes.hold(False)
    
    def setData(self, data):
        
        dates = data.date
        close = data.close
        
        self.ax.plot_date(dates, close, "-")
        self.draw()
