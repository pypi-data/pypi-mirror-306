import math

def power(a, b):
    return a ** b

def sqrt(a):
    if a < 0:
        raise ValueError("Cannot take the square root of a negative number")
    return math.sqrt(a)

def factorial(n):
    if n < 0:
        raise ValueError("Cannot take the factorial of a negative number")
    if n == 0:
        return 1
    return n * factorial(n - 1)