from calculator.advanced_operations import factorial, power

def log_base(n, base, terms=100):
    if n <= 0 or base <= 0:
        raise ValueError("Math domain error: log(x) is only defined for x > 0 and base > 0.")
    if base == 1:
        raise ValueError("Math domain error: log base 1 is undefined.")

    ln_n = natural_log(n, terms)
    ln_base = natural_log(base, terms)
    return ln_n / ln_base


def ln_1_plus_x(x, terms=100):
    # Calculate ln(1 + x) using the Taylor series expansion
    result = 0
    for n in range(1, terms + 1):
        term = power(-1, n + 1) * power(x, n) / n
        result += term
    return result


def natural_log(x, terms=100):
    if x <= 0:
        raise ValueError("Math domain error: ln(x) is only defined for x > 0.")
    e_approx = 2.7182
    k = 0
    while x > e_approx:
        x /= e_approx
        k += 1
    while x < 1 / e_approx:
        x *= e_approx
        k -= 1

    return ln_1_plus_x(x - 1, terms) + k


def exponential(x):
    e_approx = 2.7182
    return e_approx ** x
