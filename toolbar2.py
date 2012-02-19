from PySide.QtGui  import *
from globals       import *

from button        import Button

class Toolbar2(QHBoxLayout):
    """Toolbar for technicals/view adjustment appears after main graph area"""

    def __init__(self, parent=None):
        super(Toolbar2, self).__init__(None)

        self.control = parent
        
        label = QLabel("Technicals")
        combo = QComboBox()
        add   = Button(combo, "add.png", "AddTechnical")
        move  = Button(parent, "remove.png", "SlideView", True)

        combo.addItems(TECHNICALS.keys())

        map(self.addWidget, [label, combo, add])
        self.addStretch()
        self.addWidget(move)
        self.addStretch()

        move.signal.connect(self.adjustView)
        add.signal.connect(self.addTechnical)

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
            


if __name__ == "__main__":
    import control
