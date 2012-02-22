if __name__ == "__main__":
    import pyStocker

from PySide.QtGui import *
from numpy        import (arange,
                          diff,
                          pi,
                          sin,
                          zeros_like)

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import os

class Graph(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=10, height=10, dpi=100):

        figure = Figure(figsize=(width, height), dpi=dpi)
        figure.subplots_adjust(left   = 0.0,
                               right  = 1.0,
                               top    = 1.0,
                               bottom = 0.0,
                               wspace = 0.0,
                               hspace = 0.0)
        super(Graph, self).__init__(figure)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.axPri = figure.add_subplot(111)
        self.axVol = self.axPri.twinx()

        self.axPri.axes.hold(False)
        self.axVol.axes.hold(False)

        figure.canvas.mpl_connect("motion_notify_event", self.motionNotifyEvent)

    def setData(self, data):

        fillcolor   = 'darkgoldenrod'
        self.data   = data
        self.dates  = data.date
        self.close  = data.close
        self.volume = (self.close*data.volume)/1e6  # dollar volume/millions
        vmax        = self.volume.max()

        self.axVol.set_ylim(0, 5 * vmax)
        self.axVol.fill_between(self.dates,
                                self.volume,
                                0,
                                label='Volume',
                                facecolor=fillcolor,
                                edgecolor=fillcolor)

        self.axPri.plot_date(self.dates, self.close, "-")
        self.axPri.set_yscale("log")

        self.dataSize = data.size
        print data[0]
        print data[-1]

        self.draw()

    def motionNotifyEvent(self, event):

        try:
            factor = float(self.dataSize)/(self.geometry().width()-1)
            print self.data[int(round(event.x * factor, 0))]
        except(AttributeError, IndexError):
            pass

