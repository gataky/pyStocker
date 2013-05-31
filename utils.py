# encoding: utf-8

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#


if __name__ == "__main__":
    import pyStocker

from PySide.QtGui  import *
from PySide.QtCore import *
from globals       import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure                  import Figure

import os
import re
import sys
import code
import matplotlib.finance as finance
import matplotlib.mlab    as mlab
import urllib2
import datetime
import atexit
import pandas

from IPython.zmq.ipkernel import IPKernelApp
from IPython.lib.kernel import find_connection_file
from IPython.frontend.qt.kernelmanager import QtKernelManager
from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.config.application import catch_config_error

#~ Setup for abstract api calls
import talib
for func in talib.func.__all__:
    _ = talib.abstract.Function(func)
from talib.abstract import *

#~ Tooltip setup
palette = QToolTip.palette()
palette.setColor(QPalette.ToolTipText, QColor("black"))
QToolTip.setPalette(palette)

settings = QSettings("settings.conf", QSettings.NativeFormat)
settings.value("Terminal/width", 500)

tooltips = {
    "search"  :"<p><b>Search</b>: Search for the ticket entered.</p>",
    "terminal":"<p><b>Terminal</b>: Show the python terminal.</p>",
    "help"    :"<p><b>Help</b>: Help decuments.</p>",
    "new"     :"<p><b>New</b>: Create a new back-test.</p>",
    "save"    :"<p><b>Save</b>: Save the current back-test.</p>",
    "pref"    :"<p><b>Preferences</b>: Customize PyStocker.</p>",
    "open"    :"<p><b>Open</b>: Open a previous back-test.</p>",

    #~ Techincal button tooltips
    "bottom":"<p><b>Bottom</b>: Move to the bottom of the technical stack.</p>",
    "down"  :"<p><b>Down</b>: Move down one in the stack.</p>",
    "up"    :"<p><b>Up</b>: Move up one in the stack.</p>",
    "top"   :"<p><b>Top</b>: Move to the top of the technical the stack.</p>",
    "stop"  :"<p><b>Stop</b>: Remove the technical from the stack.</p>",
    }

class Button(QLabel):
    """---- ---- ---- ---- Custom Icon Button
    Button made from a QLabel where we use an image insted of text. Image is
    the name of the file to be used as the image (stord in the imgs dir), ID
    is the "action" (one word discription) of what the button does.  ID is used
    elsewhere for action control ***should replace with objectName***.
    Moveable is if the button is "moveable" meaning this is a sliding button,
    the button itself will not move but mouseTracking is set to True. This
    option is used for sliding resize widget bars.
    """

    clicked = Signal(list)

    def __init__(self, parent=None, image=None, id=None, moveable=False,
                                                                tooltip=None):
        super(Button, self).__init__(parent)

        self.image = os.path.join("imgs", image)
        self.setPixmap(QPixmap(self.image))

        self.parent   = parent
        self.id       = id
        self.holding  = False # is the button being held?
        self.moveable = moveable

        self.setToolTip(tooltip)

        if moveable:
            self.setMouseTracking(True)

    def mousePressEvent(self, event):

        kwargs = {"id"    : self.id,
                  "parent": self.parent,
                  "pos"   : event.pos()}
        #~ Connected:
        #~ Emits to :
        self.clicked.emit(kwargs)
        self.holding = True

    def mouseMoveEvent(self, event):

        if self.holding and self.moveable:
            kwargs = {"id"    : self.id,
                      "parent": self.parent,
                      "pos"   : event.pos()}
            #~ Connected:
            #~ Emits to :
            self.clicked.emit(kwargs)

    def mouseReleaseEvent(self, event):
        self.holding = False

class StockStats(QHBoxLayout):

    def __init__(self, parent):
        super(StockStats, self).__init__()

        self.symbol = QLabel("")
        self.open   = QLabel("")
        self.high   = QLabel("")
        self.low    = QLabel("")
        self.close  = QLabel("")
        self.volume = QLabel("")
        self.delta  = QLabel("")
        self.points = QLabel("")

        self.addWidget(self.symbol)
        self.addWidget(self.open)
        self.addWidget(self.high)
        self.addWidget(self.low)
        self.addWidget(self.close)
        self.addWidget(self.volume)
        self.addStretch()
        self.addWidget(self.delta)
        self.addWidget(self.points)

    def initializeStats(self, symbol, data):
        self.symbol.setText(symbol)
        self.setRangeStats(data)

    def setDayStats(self, data):
        self.open.setText("O:{:.2f}, ".format(data["open"]))
        self.high.setText("H:{:.2f}, ".format(data["high"]))
        self.low.setText("L:{:.2f}, ".format(data["low"]))
        self.close.setText("C:{:.2f}, ".format(data["close"]))
        self.volume.setText("V:{} ".format(data["volume"]))

    def setRangeStats(self, data):
        delta = data.irow(-1)["close"] - data.irow(0)["close"]
        points = delta/float(data.irow(0)["close"]) * 100
        self.delta.setText("{:+.2f} ".format(delta))
        self.points.setText("{:+.2f}% ".format(points))


class Graph(FigureCanvasQTAgg):
    """---- ---- ---- ---- Graph Ticker Display
    Graph displaying the given ticker data.
    """

    def __init__(self, parent=None, width=10, height=10, dpi=100):

        figure = Figure(figsize=(width, height), dpi=dpi)
        figure.subplots_adjust(left   = 0.0,
                               right  = 1.0,
                               top    = 1.0,
                               bottom = 0.0,
                               wspace = 0.0,
                               hspace = 0.0)
        super(Graph, self).__init__(figure)
        self.control = parent
        self.figure  = figure
        # Fill the area with the graph
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.axPri = figure.add_subplot(111)
        #self.axVol = self.axPri.twinx()

        figure.canvas.mpl_connect("motion_notify_event", self.motionNotifyEvent)
        self.rangeVerticleLine = None
        self.mouseVerticleLine = None

    def setSpan(self, low, high):
        try:
            self.section = self.data[low:high+1]
            self.sectionLen = len(self.section)
        except AttributeError:
            return

        startDate = self.section.irow(0)
        stopDate  = self.section.irow(-1)
        self.control.dateRange.setDates(startDate.name, stopDate.name)
        self.setDataToGraph(self.section)
        self.control.stockStats.setRangeStats(self.section)

    def setData(self, data):
        self.data       = data
        self.section    = data[:]
        self.sectionLen = len(data)

        self.control.terminal.updateNamespace("data", data)

    def setDataToGraph(self, data):

        self.axPri.axes.hold(False)
        self.axPri.plot_date(data.index, data["close"], "-")
        self.axPri.set_yscale(Y_AXIS_SCALE)

        self.axPri.yaxis.grid(color     = Y_AXIS_GRID_COLOR,
                              linestyle = "dashed",
                              which     = "both")

        self.axPri.xaxis.grid(color     = X_AXIS_GRID_COLOR,
                              linestyle = "dashed",
                              which     = "major")

        self.axPri.set_axisbelow(True)
        self.dataSize = len(data)
        self.draw()

    def motionNotifyEvent(self, event):
        try:
            factor = float(self.dataSize)/(self.geometry().width()-1)
        except AttributeError:
            #~ Data not yet set
            return
        index = int(round(event.x * factor, 0))
        #~ Filter out event.x positions that are out of range and give errors
        if (index >= self.sectionLen) or (index <= -1):
            return
        xValue = self.section.irow(index).name
        self.setVerticleLine(xValue, "mouse")
        self.control.stockStats.setDayStats(self.section.irow(index))

    def setVerticleLine(self, point, lineType="range"):
        #~ If the left slider is left alone on start and the right slider had
        #~ moved, then if we try and adjust the left slider we'll get zero for
        #~ point which will become the last element in the data and squish the
        #~ graph to the right then redraw it.
        if lineType == "range":
            if point <= 0:
                point += 1
            x = self.data.irow(point-1).name
            #~ Don't draw the graph when sliding outside of data currently shown
            #~ Once the mouse is released the graph will be reploted.
            lowerDate = self.section.irow(0)
            upperDate = self.section.irow(-1)
            if (x <= lowerDate.name) or (x >= upperDate.name):
                return

            if self.rangeVerticleLine:
                try:
                    self.rangeVerticleLine.remove()
                except ValueError:
                    pass
            self.rangeVerticleLine = self.axPri.axvline(x=x,
                                                        linewidth=3,
                                                        alpha=.75,
                                                        linestyle="-",
                                                        color="red")

        elif lineType == "mouse":
            x = point
            if self.mouseVerticleLine:
                try:
                    self.mouseVerticleLine.remove()
                except ValueError:
                    pass
            self.mouseVerticleLine = self.axPri.axvline(x=x,
                                                        linewidth=3,
                                                        alpha=.75,
                                                        linestyle="-",
                                                        color="green")
        try:
            self.draw()
        except RuntimeError:
            pass


class DateRange(QHBoxLayout):

    def __init__(self, parent=None):
        super(DateRange, self).__init__()

        self.control = parent
        self.start   = QLabel("")
        self.span    = QLabel("")
        self.stop    = QLabel("")
        layout1      = QHBoxLayout()
        layout2      = QHBoxLayout()

        self.addWidget(self.start)
        self.addStretch()
        self.addWidget(self.span)
        self.addStretch()
        self.addWidget(self.stop)

    def setDates(self, start, stop):
        self.start.setText(start.ctime().replace("00:00:00 ", ""))
        self.stop.setText(stop.ctime().replace("00:00:00 ", ""))
        span = stop - start
        #~ self.span.setText(u"↽{}⇀".format(str(span.days)))
        self.span.setText(u"⇐{}⇒".format(str(span.days)))

    def updateDates(self, low, high):
        try:
            low  = self.control.graph.data.irow(low)[0]
            high = self.control.graph.data.irow(high-1)[0]
            self.setDates(low, high)
        except AttributeError, error:
            #~ No data has been set to the graphing area.
            pass

class RangeSlider(QSlider):
    """---- ---- ---- ---- Slider for Ranges
       This class provides a dual-slider for ranges, where there is a defined
       maximum and minimum, as is a normal slider, but instead of having a
       single slider value, there are 2 slider values.

       This class emits the same signals as the QSlider base class, with the
       exception of valueChanged
    """

    sliderMoved = Signal(int, int)

    def __init__(self, parent=None, *args):
        super(RangeSlider, self).__init__(*args)

        self.control = parent
        #self.setOrientation(Qt.Horizontal)
        self._low = self.minimum()
        self._high = self.maximum()

        self.pressed_control = QStyle.SC_None
        self.hover_control = QStyle.SC_None
        self.click_offset = 0

        # 0 for the low, 1 for the high, -1 for both
        self.active_slider = 0

    def low(self):
        return self._low

    def setLow(self, low):
        self._low = low
        self.update()

    def high(self):
        return self._high

    def setHigh(self, high):
        self._high = high
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        style = QApplication.style()

        for i, value in enumerate([self._low, self._high]):
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)

            # Only draw the groove for the first slider so it doesn't get drawn
            # on top of the existing one every time
            if i == 0:
                opt.subControls = QStyle.SC_SliderGroove|QStyle.SC_SliderHandle
            else:
                opt.subControls = QStyle.SC_SliderHandle

            if self.tickPosition() != self.NoTicks:
                opt.subControls |= QStyle.SC_SliderTickmarks

            if self.pressed_control:
                opt.activeSubControls = self.pressed_control
                opt.state |= QStyle.State_Sunken
            else:
                opt.activeSubControls = self.hover_control

            opt.sliderPosition = value
            opt.sliderValue = value
            style.drawComplexControl(QStyle.CC_Slider, opt, painter, self)

    def mouseReleaseEvent(self, event):
        #~ Connected: Control
        #~ Emits to : self.graph.setSpan
        self.sliderMoved.emit(self._low, self._high)

    def mousePressEvent(self, event):
        event.accept()

        style = QApplication.style()
        button = event.button()

        #~ In a normal slider control, when the user clicks on a point in the
        #~ slider's total range, but not on the slider part of the control the
        #~ control would jump the slider value to where the user clicked.
        #~ For this control, clicks which are not direct hits will slide both
        #~ slider parts
        if button:
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)

            self.active_slider = -1

            for i, value in enumerate([self._low, self._high]):
                opt.sliderPosition = value
                hit = style.hitTestComplexControl(style.CC_Slider,
                                                  opt,
                                                  event.pos(),
                                                  self)
                if hit == style.SC_SliderHandle:
                    self.active_slider = i
                    self.pressed_control = hit

                    self.triggerAction(self.SliderMove)
                    self.setRepeatAction(self.SliderNoAction)
                    self.setSliderDown(True)
                    break

            if self.active_slider < 0:
                self.pressed_control = QStyle.SC_SliderHandle

                xory = self.__pick(event.pos())
                self.click_offset = self.__pixelPosToRangeValue(xory)
                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self.pressed_control != QStyle.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
        new_pos = self.__pixelPosToRangeValue(self.__pick(event.pos()))
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        if self.active_slider < 0:
            offset = new_pos - self.click_offset
            self._high += offset
            self._low += offset
            if self._low < self.minimum():
                diff = self.minimum() - self._low
                self._low += diff
                self._high += diff
            if self._high > self.maximum():
                diff = self.maximum() - self._high
                self._low += diff
                self._high += diff
        elif self.active_slider == 0:
            if new_pos >= self._high:
                new_pos = self._high - 1
            self._low = new_pos
        else:
            if new_pos <= self._low:
                new_pos = self._low + 1
            self._high = new_pos

        self.click_offset = new_pos
        self.update()

        self.control.dateRange.updateDates(self._low, self._high)

        if self.active_slider == 1:
            self.control.graph.setVerticleLine(self._high)
        elif self.active_slider == 0:
            self.control.graph.setVerticleLine(self._low)

    def __pick(self, pt):
        if self.orientation() == Qt.Horizontal:
            return pt.x()
        else:
            return pt.y()


    def __pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        style = QApplication.style()

        gr = style.subControlRect(style.CC_Slider,
                                  opt,
                                  style.SC_SliderGroove,
                                  self)

        sr = style.subControlRect(style.CC_Slider,
                                  opt,
                                  style.SC_SliderHandle,
                                  self)

        if self.orientation() == Qt.Horizontal:
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
        else:
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1

        return style.sliderValueFromPosition(self.minimum(),
                                             self.maximum(),
                                             pos-slider_min,
                                             slider_max-slider_min,
                                             opt.upsideDown)


class Technicals(QWidget):
    """Widget that houses all technical groupboxes, appears in ScrollArea"""

    def __init__(self, parent=None):
        super(Technicals, self).__init__(parent)
        self.layout  = QVBoxLayout(self)
        self.widgets = []
        self.control = parent
        # don't allow added widgets to expand in size
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)

    def addTechnical(self, technicalName):
        tech = self.Technical(self, technicalName)
        self.layout.addWidget(tech)
        self.widgets.append(tech)


    class Technical(QGroupBox):
        """Handles all actions for one technical"""

        def __init__(self, parent=None, techName=None):
            super(Technicals.Technical, self).__init__(parent)

            self.technicals = parent
            self.groupName  = techName
            self.setTitle(techName)

            # Expand on H compress on V
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

            layout = QVBoxLayout(self)
            layout.addLayout(Technicals.TechBar(self, TECHNICALS[techName]))

            graph = QGraphicsView()
            graph.setFixedHeight(25)
            layout.addWidget(graph)

        def mouseDoubleClickEvent(self, event):
            changeName = ChangeName(self, self.groupName)


    class TechBar(QHBoxLayout):
        """Toolbar that accepts technical parameters and placement buttons"""

        def __init__(self, parent=None, parameters=None):
            super(Technicals.TechBar, self).__init__(None)

            self.technical = parent
            self.setParameters(parameters)

            for button in ["bottom", "down", "up", "top", "stop"]:
                image = button + ".png"
                buttonObj = Button(parent, image, button.capitalize(),
                                   tooltip=tooltips.get(button))
                self.addWidget(buttonObj)
                buttonObj.clicked.connect(self.handle)

        def setParameters(self, params):

            for key in xrange(len(params)-1):
                parm = getattr(sys.modules[__name__], params[key]["class"])
                parm = parm()

                for method in params[key]["methods"]:
                    # method == [class method, [args]]
                    try:
                        # method takes one arg
                        getattr(parm, method[0]).__call__(method[1])
                    except TypeError:
                        # method takes more than one arg thus the "*". This will
                        # unpack method[1] into the method.
                        getattr(parm, method[0]).__call__(*method[1])

                self.addWidget(QLabel(params[key]["name"]))
                self.addWidget(parm)

            update = Button(self.technical, "refresh.png", "UpdateTech")
            update.clicked.connect(self.updateTechnical)

            self.addWidget(update)
            self.addStretch()

        def handle(self, kwargs):

            parent  = kwargs["parent"]
            id      = kwargs["id"]
            if id == "Stop":
                self.removeTechnical(parent, id)
            else:
                self.moveTechnicals(parent, id)

        def updateTechnical(self, kwargs):
            print kwargs

        def moveTechnicals(self, parent, id):

            widgets = parent.technicals.widgets
            index   = widgets.index(parent)

            if   id == "Up" and index <> 0:
                newIndex = index - 1
            elif id == "Down" and index <> len(widgets) - 1:
                newIndex = index + 1
            elif id == "Top" and index <> 0:
                newIndex = 0
            elif id == "Bottom" and index <> len(widgets) - 1 :
                newIndex = len(widgets)
            else:
                return

            map(parent.technicals.layout.removeWidget, widgets)
            widgets.insert(newIndex, widgets.pop(index))
            map(parent.technicals.layout.addWidget, widgets)

        def removeTechnical(self, parent, id):

            parent.technicals.layout.removeWidget(parent)
            parent.setParent(None)
            parent.technicals.widgets.remove(parent)


class Toolbar1(QHBoxLayout):
    """Toolbar at the top of the program"""

    def __init__(self, parent=None):
        super(Toolbar1, self).__init__(None)

        self.control = parent

        symbol = QLabel("Ticker")
        entry  = TickerEntry(self)
        entry.setFixedWidth(75)

        search = Button(entry, "search.png", "GetSymbolData",
                        tooltip=tooltips.get("search"))

        new    = Button(parent, "new.png", "New",
                        tooltip=tooltips.get("new"))

        open   = Button(parent, "open.png", "Open",
                        tooltip=tooltips.get("open"))

        save   = Button(parent, "save.png", "Save",
                        tooltip=tooltips.get("save"))

        pref   = Button(parent, "preferences.png", "Preferences",
                        tooltip=tooltips.get("pref"))

        term   = Button(parent, "terminal.png", "Terminal",
                        tooltip=tooltips.get("terminal"))

        help   = Button(parent, "help.png", "Help",
                        tooltip=tooltips.get("help"))

        map(self.addWidget, [symbol, entry, search])
        self.addStretch()
        map(self.addWidget, [new, open, save])
        self.addStretch()
        map(self.addWidget, [pref, term, help])

        search.clicked.connect(self.getSymbolData)
        new.clicked.connect(self.new)
        save.clicked.connect(self.save)
        open.clicked.connect(self.open)
        pref.clicked.connect(self.preferences)
        term.clicked.connect(self.terminal)
        help.clicked.connect(self.help)

    def getSymbolData(self, event):
        # event can either be a dict of an QObject depending on wheather the
        # user clicked the search button or pressed enter.
        if isinstance(event, QObject):
            lineEdit = event
        elif isinstance(event, dict):
            lineEdit = event["parent"]

        end    = datetime.datetime.today()
        start  = end - datetime.timedelta(weeks=YEARS_OF_DATA * 52.177457)
        ticker = lineEdit.text().upper()

        # Check that something was entered in the ticker
        if not ticker:
            return

        for attempt in xrange(GET_DATA_ATTEMPTS):
            try:
                # a numpy record array with fields:
                # date, open, high, low, close, volume, adj_close
                with finance.fetch_historical_yahoo(ticker, start, end) as fh:
                    data = mlab.csv2rec(fh)
                data.sort()
                data = pandas.DataFrame(data)
                data = data.set_index("date")
            except urllib2.HTTPError:
                if attempt == 2:
                    return
            finally:
                try:
                    data
                    break
                except Exception, error:
                    return

        self.control.sliders.setMinimum(0)
        self.control.sliders.setMaximum(len(data))
        self.control.sliders.setLow(0)
        self.control.sliders.setHigh(len(data))

        self.control.graph.setData(data)
        self.control.graph.setDataToGraph(data)

        self.control.dateRange.setDates(data.irow(0).name, data.irow(-1).name)
        self.control.stockStats.initializeStats(ticker, data)

    def new(self, kwargs):
        print kwargs

    def save(self, kwargs):
        print kwargs

    def open(self, kwargs):
        print kwargs

    def preferences(self, kwargs):
        print kwargs

        self.foo = Preferences(self.control)


    def terminal(self, kwargs):
        self.control.terminalVisible = not self.control.terminalVisible
        if self.control.terminalVisible:
            self.control.terminal.show()
        else:
            self.control.terminal.hide()

    def help(self, kwargs):
        print kwargs


class Toolbar2(QHBoxLayout):
    """Toolbar for technicals/view adjustment appears after main graph area"""

    def __init__(self, parent=None):
        super(Toolbar2, self).__init__(None)

        self.control = parent

        label = QLabel("Technicals")
        combo = QComboBox()
        add   = Button(combo, "add.png", "AddTechnical")
        move  = Button(parent, "remove.png", "SlideView", True)
        funcs = map(lambda name: eval("{}.info['display_name']".format(name)),
                                                            talib.func.__all__)
        combo.addItems(funcs)
        combo.setFixedWidth(200)

        map(self.addWidget, [label, combo, add])
        self.addStretch()
        self.addWidget(move)
        self.addStretch()

        move.clicked.connect(self.adjustView)
        add.clicked.connect(self.addTechnical)

    def addTechnical(self, kwargs):

        parent = kwargs["parent"]
        name   = parent.currentText()
        self.control.scrollArea.addTechnical(name)

    def adjustView(self, kwargs):
        if kwargs["id"] == "SlideView":
            parent  = kwargs["parent"]
            dy      = kwargs["pos"].y()
            height  = parent.scrollArea.geometry().size().height()
            max     = parent.size().height() * MAX_HEIGHT_FACTOR
            height -= dy
            # don't allow setting too high and can't have negative numbers
            if height >= max or height <= 0:
                return
            parent.scrollArea.setFixedHeight(height)


class TickerEntry(QLineEdit):

    def __init__(self, parent=None):
        super(TickerEntry, self).__init__(None)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            self.parent.getSymbolData(self)
        super(TickerEntry, self).keyPressEvent(event)


class QIPythonWidget(RichIPythonWidget):

    class KernelApp(IPKernelApp):
        @catch_config_error
        def initialize(self, argv=[]):
            super(QIPythonWidget.KernelApp, self).initialize(argv)
            self.kernel.eventloop = self.loop_qt4_nonblocking
            self.kernel.start()
            self.start()

        def loop_qt4_nonblocking(self, kernel):
            kernel.timer = QTimer()
            kernel.timer.timeout.connect(kernel.do_one_iteration)
            kernel.timer.start(1000*kernel._poll_interval)

        def get_connection_file(self):
            return self.connection_file

        def get_user_namespace(self):
            return self.kernel.shell.user_ns

    def __init__(self, parent=None, colors="linux", namespace=None,
                       visible=True, width=900):
        super(QIPythonWidget, self).__init__()
        self.control = parent
        self.app = self.KernelApp.instance(argv=[])
        self.app.initialize()
        self.set_default_style(colors=colors)
        self.connect_kernel(self.app.get_connection_file())
        self.set_namespace(namespace)
        self.setVisible(visible)

    def set_namespace(self, namespace):
        if namespace and isinstance(namespace, dict):
            current = self.get_user_namespace()
            current.update(namespace)
            self.app.shell.init_create_namespaces(user_ns=current)

    def connect_kernel(self, conn, heartbeat=False):
        km = QtKernelManager(connection_file=find_connection_file(conn))
        km.load_connection_file()
        km.start_channels(hb=heartbeat)
        self.kernel_manager = km
        atexit.register(self.kernel_manager.cleanup_connection_file)

    def get_user_namespace(self):
        return self.app.get_user_namespace()

    def closeEvent(self, event):
        self.control.terminalVisible = False

    def updateNamespace(self, key, value):
        namespace = self.get_user_namespace()
        namespace[key] = value


class ChangeName(QDialog):

    def __init__(self, parent, currentName):
        super(ChangeName, self).__init__()
        top     = QVBoxLayout(self)
        layout  = QHBoxLayout()
        layoutb = QHBoxLayout()
        ok      = QPushButton("OK")
        cancle  = QPushButton("Cancle")

        self.parent  = parent
        self.newName = QLineEdit()
        self.newName.setPlaceholderText(currentName)

        layout.addWidget(self.newName)
        layoutb.addWidget(ok)
        layoutb.addWidget(cancle)
        top.addLayout(layout)
        top.addLayout(layoutb)

        ok.clicked.connect(self.changeName)
        cancle.clicked.connect(self.reject)

        self.exec_()

    def changeName(self):
        name = self.newName.text()
        if name:
            self.parent.setTitle(name)
        self.reject()
