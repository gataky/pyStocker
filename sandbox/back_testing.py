
import pandas as pd
import numpy  as np
import talib  as ta

from tradeking import api as tk


response = tk.market_historical_search("goog", "daily", "2013-01-01", "2013-06-01")


class Backtest(list):

    def __init__(self, techs):
        super(Backtest, self).__init__()
        if isinstance(techs, list):
            self.extend(techs)
        elif isinstance(techs, Technical):
            self.append(techs)

    def run(self):
        map(lambda tech: tech(), self)


class Technical(ta.abstract.Function):

    columns = ["open", "high", "low", "close", "volume"]

    def __init__(self, function, data):
        super(Technical, self).__init__(function.upper())
        self.__setData(data)
        self.__setName(function)

    def __format__(self, data):
        """Convert a panda data frame object into a valid ta-lib input"""
        return {k: data[k].values.astype(float) for k in self.columns}

    def __call__(self, data=None):
        if data:
            self.__setData(data)
        output = super(Technical, self).run()
        self.data["output"] = pd.DataFrame(output, index=self.data.index)
        return output

    def __setData(self, data):
        self.data = pd.DataFrame(data).set_index("date").astype(float)
        super(Technical, self).set_input_arrays(self.__format__(self.data))
        return True

    def __setName(self, name):
        self.name = name

    def __getName(self):
        name   = self.info["name"]
        params = self.info["parameters"]
        params = "_".join(map(lambda x: "{}:{}".format(*x), params.items()))
        self.__setName("{}_{}".format(name, params))
        return self.name

    def __updateName(self):
        self.__getName()

    def __repr__(self):
        return self.__getName()

    def __str__(self):
        return self.__repr__()

    def run(self, data=None):
        return self.__call__(data)

    def setBacktest(self, backtest):
        self.backtest = backtest
        return True

    def setFunctionArgs(self, **kwargs):
        self.set_function_args(kwargs)
        self.__updateName()
        return True

    def setInputArrays(self, data):
        if data:
            return self.__setData(data)
        return True

    def setInputNames(self, **kwargs):
        self.set_input_names(kwargs)
        self.__updateName()
        return True

    def setParameters(self, **kwargs):
        self.set_parameters(kwargs)
        self.__updateName()
        return True

    @staticmethod
    def supported():
        return ta.get_function_groups()


data = response.json()["response"]["timeseries"]["series"]["data"]
sma1 = Technical("sma", data)
sma2 = Technical("sma", data)


sma2.setParameters(timeperiod=10)
print sma2

b = Backtest([sma1, sma2])
print b

