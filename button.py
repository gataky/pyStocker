from PySide.QtGui  import *
from globals       import *
from preferences   import Preferences

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
            print self.id, self.parent, self.parent.text()

        elif self.id == "Terminal":
            print self.id, self.parent

        elif self.id == "AddTechnical":
            name = self.parent.currentText()
            self.yaya.scrollArea.addTechnical(name)

        elif self.id == "SlideView":
            self.holding = True
            
        elif self.id in ["Up", "Down", "Top", "Bottom"]:            
            self.moveTechnicals()
            
        elif self.id == "Stop":
            self.removeTechnical()

        elif self.id == "UpdateTech":
            print self.id, self.parent

        elif self.id == "Preferences":
            print self.id, self.parent
            #Preferences(self.parent)
            

            
    def mouseMoveEvent(self, event):

        if self.holding:
            dy      = event.pos().y()
            height  = self.parent.scrollArea.geometry().size().height()
            max     = self.parent.size().height() * MAX_HEIGHT_FACTOR
            height -= dy            
            # don't allow setting too high and can't have negative numbers
            if height >= max or height <= 0:
                return
            self.parent.scrollArea.setFixedHeight(height)

    def mouseReleaseEvent(self, event):
        self.holding = False

    def moveTechnicals(self):

        widgets = self.parent.technicals.widgets
        index   = widgets.index(self.parent)
        
        if   self.id == "Up" and index <> 0:
            newIndex = index - 1
        elif self.id == "Down" and index <> len(widgets) - 1:
            newIndex = index + 1
        elif self.id == "Top" and index <> 0:
            newIndex = 0
        elif self.id == "Bottom" and index <> len(widgets) - 1 :
            newIndex = len(widgets)
        else:
            return
        
        map(self.parent.technicals.layout.removeWidget, widgets)
        widgets.insert(newIndex, widgets.pop(index))
        map(self.parent.technicals.layout.addWidget, widgets)

    def removeTechnical(self):
        
        self.parent.technicals.layout.removeWidget(self.parent)
        self.parent.setParent(None)
        self.parent.technicals.widgets.remove(self.parent)


if __name__ == "__main__":
    import control
