from PySide.QtGui  import *
from PySide.QtCore import *
from globals       import *
from preferences   import Preferences
from interpreter   import Interpreter

import os

class Button(QLabel):
    """Custom icon buttons"""

    signal = Signal(list)

    def __init__(self, parent=None, image=None, id=None, moveable=False):
        super(Button, self).__init__(parent)

        self.image    = os.path.join("imgs", image)
        self.parent   = parent
        self.id       = id
        self.holding  = False # is the button being held?
        self.moveable = moveable

        self.setPixmap(QPixmap(self.image))
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
         
        kwargs = {"id"    : self.id, 
                  "parent": self.parent,
                  "pos"   : event.pos()}
        self.signal.emit(kwargs)
        self.holding = True
            
    def mouseMoveEvent(self, event):
        
        if self.holding and self.moveable:
            kwargs = {"id"    : self.id, 
                      "parent": self.parent,
                      "pos"   : event.pos()}
            self.signal.emit(kwargs)

    def mouseReleaseEvent(self, event):
        self.holding = False

if __name__ == "__main__":
    import control
