def power(x, y):
    if y == 0:
        return 1
    else:
        return x ** y
def square_root(x):
    return (x ** 0.5)
def factorial(num):
    if num == 1:
        return 1
    else:
        return factorial(num - 1) * num