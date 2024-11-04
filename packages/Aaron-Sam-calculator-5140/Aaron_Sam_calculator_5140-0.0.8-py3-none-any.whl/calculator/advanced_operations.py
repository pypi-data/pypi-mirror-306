def power (a, b):
    return a ** b

def sqrt (a):
    return a ** 0.5

def factorial (a):
    if a == 0:
        return 1
    else:
        return a * factorial(a-1)