from calculator.advanced_operations import factorial, power

def sine(x, terms=10):
    result = 0
    for i in range(terms):
        sign = (-1) ** i
        result += sign * power(x, 2 * i + 1) / factorial(2 * i + 1)
    return result

def cosine(x, terms=10):
    result = 0
    for i in range(terms):
        sign = (-1) ** i
        result += sign * power(x, 2 * i) / factorial(2 * i)
    return result

def tangent(x, terms=10):
    sin_x = sine(x, terms)
    cos_x = cosine(x, terms)
    if cos_x == 0:
        raise ValueError("Tangent is undefined for this value of x.")
    return sin_x / cos_x

