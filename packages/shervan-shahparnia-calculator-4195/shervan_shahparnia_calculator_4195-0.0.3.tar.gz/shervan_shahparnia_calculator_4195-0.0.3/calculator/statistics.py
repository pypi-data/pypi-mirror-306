import statistics

def mean(data):
    return statistics.mean(data)

def median(data):
    return statistics.median(data)

def mode(data):
    try:
        return statistics.mode(data)
    except statistics.StatisticsError as e:
        return str(e)

def standard_deviation(numbers):
    return statistics.stdev(numbers)

