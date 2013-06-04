
import pandas as pd
import numpy  as np

from tradeking      import api as tk
from talib.abstract import *

abstracts = __import__("talib.abstract", fromlist=["*"])

response = tk.market_historical_search("goog", "daily", "2013-01-01", "2013-06-01")


TechnicalInfo = """group       : {group}
display_name: {display_name}
name        : {name}
input_names : {input_names}
parameters  : {parameters}
output_flags: {output_flags}
output_names: {output_names}"""

class Technical(pd.DataFrame):

    def __new__(cls, *args, **kwargs):
        return pd.DataFrame.__new__(cls, *args, **kwargs)

    def __init__(self, name, *args, **kwargs):
        super(Technical, self).__init__(*args, **kwargs)
        self.name = name

    def __format__(self):
        """Send in any data that can be converted to a Pandas DataFrame object
        with at atleast open, high, low, close and volume columns and this will
        convert the data into a form that is accepted by ta-lib
        """
        return {k: self[k].values.astype(float) for k in self}

    def setFunction(self, name):
        self.function = abstracts.__getattribute__(name.upper())

    def run(self):
        _ = __format__


data = response.json()["response"]["timeseries"]["series"]["data"]

sma  = Technical("sma", data)
#~ sma2(response.json()["response"]["timeseries"]["series"]["data"])


