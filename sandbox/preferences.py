from PySide.QtGui import *


class Preferences(QDialog):
    
    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        
        layout = QVBoxLayout(self)        
        layout.addWidget(Tabs())

        self.exec_()


class Tabs(QTabWidget):
    
    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
        
        self.setTabPosition(QTabWidget.West)
        self.addTab(QLabel("foo"), "foo")
        

class TopLayout(QVBoxLayout):
    
    def __init__(self, parent=None):
        super(TopLayout, self).__init__(None)
        
        self.addWidget(QCheckBox("Remember user settings", parent))

        
class ButtonLayout(QHBoxLayout):
    
    def __init__(self, parent=None):
        super(ButtonLayout, self).__init__(None)

        self.addWidget(QPushButton("Cancle", parent))
        self.addWidget(QPushButton("Save", parent))
        self.addWidget(QPushButton("Save && Exit", parent))


if __name__ == "__main__":
    import control
