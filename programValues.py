from PySide.QtCore import *
from PySide.QtGui  import *


# Percentage of the screen that the Technical view will be allowed to take up.
MAX_HEIGHT_FACTOR = .5

# all information relating to TA-lib is defined here
TECHNICALS = {
# ---------------------------------------------------------------------------- #
"Tech Name" :                                                                   # Name of the Tech
{
    "abbr"  : "TN",                                                             # Tech accronim
    0       : {                                                                 # 1st parameter
                "name"    : "One",                                              # parameter name
                "class"   : "QLineEdit",                                        # parameter class type
                "methods" : [["setText", "Hello!"],                             # methods for class
                             ["setSizePolicy", (QSizePolicy.Minimum,
                                                QSizePolicy.Fixed)],]
                },

    1       : {                                                                 # nth parameter
                "name"    : "Two",
                "class"   : "QPushButton",
                "methods" : [["setText", "Push Me"],
                             ["setSizePolicy", (QSizePolicy.Minimum,
                                                QSizePolicy.Fixed)],]
                },
},
# ---------------------------------------------------------------------------- #
"Another Tech":
{
    "abbr"  : "AT",

    0       : {
                "name"    : "1A",
                "class"   : "QLineEdit",
                "methods" : [["setText", "Text for 1A"],
                             ["setSizePolicy", (QSizePolicy.Minimum,
                                                QSizePolicy.Fixed)],]
                },

    1       : {
                "name"    : "2B",
                "class"   : "QLineEdit",
                "methods" : [["setText", "Text for 2b"],
                             ["setSizePolicy", (QSizePolicy.Minimum,
                                                QSizePolicy.Fixed)],]
                },
},
# ---------------------------------------------------------------------------- #
}
