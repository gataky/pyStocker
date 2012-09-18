
class Trending(object):

    def __init__(self, data, reversal, data_is_reverse=False):

        data = map(float, data)
        if data_is_reverse:
            self._data = data[::-1]
        else:
            self._data = data

        self._reversal = reversal

        self._max = min(data)
        self._min = max(data)

        self._trend = []


    def _initialize_trend(self):

        delta = self._data[1] - self._data[0]
        if delta >= 0:
            return True, [True, True]
        else:
            return False, [False, False]


    def setData(self, data):
        self._data = data


    def setReversal(self, value):
        self._reversal = float(value)


    def getReversal(self):
        return self._reversal


    def getTrend(self):
        for i, point in enumerate(self._data[1:]):

            if i == 0:
                trend, self._trend = self._initialize_trend()
                previous = point
                continue

            delta = point - previous

            if trend and delta > 0:
                if point > self._max:
                    self._max = point

            elif trend and delta < 0:
                if abs(self._max - point) >= self._reversal:
                    trend = not trend
                    self._min = point

            elif not trend and delta > 0:
                if abs(self._min - point) >= self._reversal:
                    trend = not trend
                    self._max = point

            elif not trend and delta < 0:
                if point < self._min:
                    self._min = point

            self._trend.append(trend)
            previous = point

        return self._trend
