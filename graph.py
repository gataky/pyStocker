if __name__ == "__main__":
    import pyStocker

from PySide.QtGui import *
from globals      import *
from button       import Button
from numpy        import (arange,
                          diff,
                          pi,
                          sin,
                          zeros_like)

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure                  import Figure

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

        figure.canvas.mpl_connect("motion_notify_event", self.motionNotifyEvent)

    def setData(self, data):

        self.axPri.axes.hold(False)
        self.axVol.axes.hold(False)

        self.data   = data
        self.volume = (data.close * data.volume)/1e6  # dollar volume/millions

        self.axVol.set_ylim(0, 5 * data.volume.max())
        self.axVol.fill_between(data.date,
                                data.volume,
                                facecolor = VOLUME_FACE_COLOR,
                                edgecolor = VOLUME_EDGE_COLOR)

        self.axPri.plot_date(data.date, data.close, "-")
        self.axPri.set_yscale(Y_AXIS_SCALE)


        self.axPri.yaxis.grid(color     = Y_AXIS_GRID_COLOR,
                              linestyle = "dashed",
                              which     = "both")

        self.axPri.xaxis.grid(color     = X_AXIS_GRID_COLOR,
                              linestyle = "dashed",
                              which     = "major")

        self.axPri.set_axisbelow(True)
        self.dataSize = data.size

        self.draw()

    def motionNotifyEvent(self, event):

        try:
            factor = float(self.dataSize)/(self.geometry().width()-1)
            print self.data[int(round(event.x * factor, 0))]
        except(AttributeError, IndexError):
            pass

