from PySide.QtGui  import *

import datetime

# -- Start settings -- #

# Percentage of the screen that the technical view will be allowed to take up.
# .4
MAX_HEIGHT_FACTOR       = .5

# Number of attempts allowed to get ticker data {1 ... n | n <> 0}
# 2
GET_DATA_ATTEMPTS       = 1

# Color of the x-axis grid lines
# "grey"
X_AXIS_GRID_COLOR       = "grey"

# Color of the y-axis grid lines
# "grey"
Y_AXIS_GRID_COLOR       = "grey"

# Color of the volume face
# "darkgoldenrod"
VOLUME_FACE_COLOR       = "darkgoldenrod"

# Color of the volume edge
# "blue"
VOLUME_EDGE_COLOR       = "blue"

# Scale of the y-axis log/linear
# "log"
Y_AXIS_SCALE            = "log"

# Gather this much time of data in years
# 2
YEARS_OF_DATA           = 2

# Defult zoom when display is initialized. 1d, 5d, 1m, 3m, 6m, YTD, All
# "6m"
DEFAULT_ZOOM            = "6m"

# -- Stop settings -- #

# -- Start technicals -- #

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
# ---------------------------------------------------------------------------- #
"3":
{
    "abbr"  : "3",

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

# -- Stop technicals -- #
