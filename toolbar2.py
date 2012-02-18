from PySide.QtGui  import *
from globals       import *

from button        import Button

class Toolbar2(QHBoxLayout):
    """Toolbar for technicals/view adjustment appears after main graph area"""

    def __init__(self, parent=None):
        super(Toolbar2, self).__init__(None)

        label = QLabel("Technicals")
        combo = QComboBox()
        add   = Button(combo, "add.png", "AddTechnical", parent)
        move  = Button(parent, "remove.png", "SlideView")

        combo.addItems(TECHNICALS.keys())

        self.addWidget(label)
        self.addWidget(combo)
        self.addWidget(add)
        self.addStretch()
        self.addWidget(move)
        self.addStretch()


if __name__ == "__main__":
    import control
