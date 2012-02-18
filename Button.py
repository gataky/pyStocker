from PySide.QtGui import *
from programValues import *

import os

class Button(QLabel):
    """Custom icon buttons made from labels"""

    def __init__(self, parent=None, image=None, objID=None):

        super(Button, self).__init__(parent)
        self.setPixmap(QPixmap(os.path.join("imgs", image)))
        self.name    = image  # image file name
        self.objID   = objID
        self.parent  = parent
        self.holding = False  # holding the mouse button down?

        self.setMouseTracking(True)

    def mousePressEvent(self, event):

        if self.objID == "process-stop": # delete on a tech
            self.parent.setParent(None) # Technical parent -> None

        if self.objID == "slider": # minus button clicked for resizing
            self.holding = True

        if self.objID == "ticker search":
            print "getting symbol data"

        if self.objID == "terminal":
            print "open python terminal"

        if self.objID == "go-up":
            print "go-up"
            print self.parent.technicals.scroll.widget().layout.children()

    def mouseMoveEvent(self, event):

        if self.holding:
            dy        = event.pos().y()
            height    = self.parent.scroll.geometry().size().height() - dy
            maxHeight = self.parent.size().height() * MAX_HEIGHT_FACTOR
            # don't allow setting too high and can't have negative numbers
            if height >= maxHeight or height <= 0:
                return
            self.parent.scroll.setFixedHeight(height)

    def mouseReleaseEvent(self, event):

        if self.holding:
            self.holding = False



if __name__ == "__main__":
    import test
