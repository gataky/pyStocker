from PySide.QtGui  import *
from programValues import *

import os

class Button(QLabel):
    """Custom icon buttons"""

    def __init__(self, parent=None, image=None, id=None, yaya=None):
        super(Button, self).__init__(parent)

        self.image   = os.path.join("imgs", image)
        self.parent  = parent
        self.id      = id
        self.yaya    = yaya  # head of the family i.e. Control
        self.holding = False # is the button being held?

        self.setPixmap(QPixmap(self.image))
        self.setMouseTracking(True)

    def mousePressEvent(self, event):

        if self.id == "GetSymbolData":
            print "get sumbol data"
            print self.id, self.parent
            print self.parent.text()

        elif self.id == "Terminal":
            print "open terminal"

        elif self.id == "AddTechnical":
            name = self.parent.currentText()
            self.yaya.scrollArea.addTechnical(name)

        elif self.id == "SlideView":
            self.holding = True
            
        elif self.id == "Bottom":
            print self.id
            
        elif self.id == "Top":
            print self.id
            
        elif self.id == "Up":
            print self.id
            
        elif self.id == "Down":
            print self.id

        elif self.id == "Stop":
            print self.id, self.parent

        elif self.id == "UpdateTech":
            print self.id, self.parent
            
            print "technicals ===="
            print self.parent.technicals.children()
            
            print "Layout ========"
            print "Empty?   ", self.parent.technicals.layout().isEmpty()
            print ".children", self.parent.technicals.layout().children()
            print ".count   ", self.parent.technicals.layout().count()
            
            print "\n\n"
            
    def mouseMoveEvent(self, event):

        if self.holding:
            dy      = event.pos().y()
            height  = self.parent.scrollArea.geometry().size().height()
            height -= dy

            maxHeight = self.parent.size().height() * MAX_HEIGHT_FACTOR
            # don't allow setting too high and can't have negative numbers
            if height >= maxHeight or height <= 0:
                return
            self.parent.scrollArea.setFixedHeight(height)

    def mouseReleaseEvent(self, event):
        self.holding = False


if __name__ == "__main__":
    import control
