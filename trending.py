
def trender(data, reversal):

    def initialize(point, previous):
        delta = point - previous
        if delta >= 0:
            return True
        else:
            return False

    data  = map(lambda x: float(x), data)

    peak  = min(data)
    dip   = max(data)
    trend = []
    for i, point in enumerate(data[1:]):

        if i == 0:
            trending = initialize(point, data[i])
            trend.extend((trending, trending))
            continue

        delta = point - data[i]

        if trending and delta > 0:
            if point > peak:
                peak = point

        elif trending and delta < 0:
            if abs(peak - point) >= reversal:
                trending = not trending
                dip = point

        elif not trending and delta > 0:
            if abs(dip - point) >= reversal:
                trending = not trending
                peak = point

        elif not trending and delta < 0:
            if point < dip:
                dip = point

        trend.append(trending)

    return trend
