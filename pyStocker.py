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


from PySide.QtGui  import *
from PySide.QtCore import *

import os
import sys
import numpy

os.environ['QT_API'] = 'pyside'
import matplotlib
matplotlib.use('Qt4Agg') # must be called before .backends or .pylab

import control # program main

app  = QApplication(sys.argv)
app.setStyle("plastique")
#app.setStyle("cleanlooks")
main = control.Control()
main.resize(600, 400)
main.show()
sys.exit(app.exec_())
