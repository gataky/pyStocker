import matplotlib.pyplot as plt
import matplotlib.dates as mdate


class PointPicker(object):
    def __init__(self,dates,values):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.lines2d, = self.ax.plot_date(dates, values, linestyle='-',picker=5)
        #~ self.fig.canvas.mpl_connect('pick_event', self.onpick)
        #~ self.fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.fig.canvas.mpl_connect('motion_notify_event', self.foo)
        self.L = None

    def foo(self, event):
        self.onpick(event)

    def onpick(self,event):
        x = event.xdata
        y = event.ydata
        if self.L:
            try:
                self.L.remove()
            except ValueError:
                pass

        try:
            self.L =  self.ax.axvline(x=x, linewidth=3, alpha=.75, linestyle="-.", color="red")
        except AttributeError:
            return
        self.fig.canvas.draw()


if __name__ == '__main__':
    import numpy as np
    import datetime

    dates=[datetime.datetime.now()+i*datetime.timedelta(days=1) for i in range(100)]
    values = np.random.random(100)

    plt.ion()
    p = PointPicker(dates,values)
    plt.show()
