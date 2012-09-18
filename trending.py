
class Trending(object):
    """Class for finding the trend of a stock given history"""

    def __init__(self, data, reversal=0.5, data_is_reverse=False):
        """data     - a list of stock prices
        reversal - amount of tolerance a stock can swing before a trend reversal

        data_is_reverse - data is given in sequential order if data[0] is your
            oldest data point then flag is False; otherwise, data[0] is your
            newest point then flag is True."""

        data = map(float, data) # incase of str points
        if data_is_reverse:
            self._data = data[::-1]
        else:
            self._data = data

        self._reversal = reversal

        self._max = min(data)
        self._min = max(data)

        self._trend = []


    def _initialize_trend(self):
        """initial trend. True == Up, False == Down"""

        delta = self._data[1] - self._data[0]
        if delta >= 0:
            return True, [True, True]
        else:
            return False, [False, False]


    def setData(self, data):
        """set the data"""

        self._data = map(float, data)


    def setReversal(self, value):
        """set the reversal value"""

        self._reversal = float(value)


    def getReversal(self):
        """get the reversal value"""
        return self._reversal


    def getTrend(self):
        """return trend of the stock with [0] being oldest data point
        True == Up, False == Down"""

        for i, point in enumerate(self._data[1:]):

            if i == 0:
                trend, self._trend = self._initialize_trend()
                previous = point # previous will be current point
                continue

            delta = point - previous # change between days

            # was trending up and closed higher
            if trend and delta > 0:
                # do we have a new high in this trend leg?
                if point > self._max:
                    self._max = point

            # was trending up and closed lower
            elif trend and delta < 0:
                # check if the point - max triggers a reversal
                if abs(self._max - point) >= self._reversal:
                    trend = not trend
                    self._min = point

            # was trending down and closed hight
            elif not trend and delta > 0:
                # check if the point - max triggers reversal
                if abs(self._min - point) >= self._reversal:
                    trend = not trend
                    self._max = point

            # was trending down and closed lower
            elif not trend and delta < 0:
                # do we have a new low in this trend leg?
                if point < self._min:
                    self._min = point

            self._trend.append(trend)
            previous = point

        return self._trend
