#!/usr/bin/python

# ================================================================
# These are some handy utility routines which I always want to
# be available in my software environment.
#
# John Kerl
# kerl.john.r@gmail.com
# 2007-03-16
# ================================================================

# ----------------------------------------------------------------
# Similar to Matlab's [start:step:end].
def mfrange(start, step, end):
    list = []
    current = start
    while (current < end):
        list.append(current)
        current += step
    return list

# ----------------------------------------------------------------
# Factorial function.
def fact(n):
    if (n <= 1):
        return n
    else:
        return n * fact(n-1)

# ----------------------------------------------------------------
# Binomial coefficients.
def binc(n, k):
    if (k > n): return 0
    if (k < 0): return 0
    if (k > int(n/2)):
        k = n - k

    rv = 1
    for j in range(0, k):
        rv *= n - j
        rv /= j + 1
    return rv
