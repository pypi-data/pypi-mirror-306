import math 

def mean (a):
    return sum(a) / len(a)

def median (a):
    a.sort()
    n = len(a)
    if n % 2 == 0:
        return (a[n//2 - 1] + a[n//2]) / 2
    else:
        return a[n//2]
    
def mode (a):
    counts = {}
    for x in a:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]

