
def mean(list):
    total = 0
    for num in list:
        total += num
    return total/len(list)

def median(list):
    return list[len(list)/2]

def mode(list):
    if not list:
        return []
    counts = {}
    max_count = 0
    for num in list:
        counts[num] = counts.get(num, 0) + 1
        if counts[num] > max_count:
            max_count = counts[num]
    modes = [num for num, count in counts.items() if count == max_count]
    return modes

def standard_deviation(list):
    n = len(list)
    if n == 0:
        return 0

    mean = sum(list) / n

    variance = sum((x - mean) ** 2 for x in list) / n
    return variance ** 0.5