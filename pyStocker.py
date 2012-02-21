from PySide.QtGui  import *
from PySide.QtCore import *

import os
import sys
import numpy

os.environ['QT_API'] = 'pyside'
import matplotlib 
matplotlib.use('Qt4Agg') # must be called before .backends or .pylab

import control

app  = QApplication(sys.argv)
main = control.Control()
main.resize(600, 400)
main.show()
sys.exit(app.exec_())
