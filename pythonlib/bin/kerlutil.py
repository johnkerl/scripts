#!/usr/bin/python -Wall

# ================================================================
# These are some handy utility routines which I always want to
# be available in my software environment.
#
# John Kerl
# kerl.john.r@gmail.com
# 2007-03-16
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import math
import cmath

# ----------------------------------------------------------------
# Factorial function.
def fact(n):
	"""fact(n): Computes n factorial."""
	if (n == 0):
		return 1
	if (n <= 1):
		return n
	else:
		#return n * fact(n-1)
		prod = 1
		while n > 1:
			prod *= n
			n -= 1
		return prod

# ----------------------------------------------------------------
# Double factorial function.
def dfact(n):
	"""dfact(n): Computes n factorial."""
	if (n == 0):
		return 1
	if (n == -1):
		return 1
	if (n == 1):
		return 1
	return n * dfact(n-2)

# ----------------------------------------------------------------
# Binomial coefficients.
def binc(n, k):
	"""binc(n, k): Computes n choose k."""
	if (k > n): return 0
	if (k < 0): return 0
	if (k > int(n/2)):
		k = n - k

	rv = 1
	for j in range(0, k):
		rv *= n - j
		rv /= j + 1
	return int(rv)

# ----------------------------------------------------------------
def printf_row(row, fmt="%11.7f"):
	"""printf_row(list, optional format)"""
	fmt_with_space = " " + fmt
	for e in row:
		print fmt_with_space % (e),
	print

# ----------------------------------------------------------------
# Similar to Matlab's [start:step:end].
def mfrange(start, step, end):
	"""mfrange(start, step, end):  Similar to Matlab's [start:step:end]."""

	# If the arguments are already float or complex, this won't hurt.
	# If they're int, they will become float.
	start *= 1.0
	step  *= 1.0
	end   *= 1.0

	list = []
	current = start
	if (step > 0):
		while (current < end):
			list.append(current)
			current += step
	elif (step < 0):
		while (current > end):
			list.append(current)
			current += step
	else:
		print >> sys.stderr, \
			"mfrange:  zero step disallowed (an infinite loop would ensue)."
		sys.exit(1)
	return list

# ----------------------------------------------------------------
# For reals or complexes (hurrah for polymorphism!):  linear from a to b.
def frange(start, end, n):
	"""frange(start, end, n):  Python's range(), for floats and complexes."""

	# If the arguments are already float or complex, this won't hurt.
	# If they're int, they will become float.
	start *= 1.0
	end   *= 1.0

	step = (end - start) / n
	list = []
	current = start
	for k in range(0, n):
		list.append(current)
		current += step
	return list

# ----------------------------------------------------------------
# Multiplicative from a to b.
# Example: mulfrange(1, 64, 6) gives [1., 2., 4., 8., 16., 32.]
def mulfrange(start, end, n):
	"""mulfrange(start, end, n):  multiplicative range() for floats."""

	# If the arguments are already float or complex, this won't hurt.
	# If they're int, they will become float.
	start *= 1.0
	end   *= 1.0

	step = (end / start) ** (1./n)
	list = []
	current = start
	for k in range(0, n):
		list.append(current)
		current *= step
	return list

# ----------------------------------------------------------------
def cphase(c):
	"""cphase(c):  returns complex phase: (-pi, +pi]."""
	return math.atan2(c.imag, c.real)

# ----------------------------------------------------------------
# frange-ish for complexes:  Re^i theta for fixed R and varying theta.
def ztrange(R, start_theta, end_theta, n, center=0+0j):
	"""ztrange(R, start_theta, end_theta, n):  R exp(i theta) for fixed R
	and varying theta."""

	# If the arguments are already float or complex, this won't hurt.
	# If they're int, they will become float.
	start_theta *= 1.0
	end_theta   *= 1.0

	list = []
	thetas = frange(start_theta, end_theta, n)
	for theta in thetas:
		list.append(center + R * cmath.exp(1j * theta))
	return list

# ----------------------------------------------------------------
# frange-ish for complexes:  Re^i theta for varying R and fixed theta.
def zrrange(start_R, end_R, theta, n):
	"""ztrange(start_R, end_R, theta, n):  R exp(i theta) for varying R
	and fixed theta."""

	# If the arguments are already float or complex, this won't hurt.
	# If they're int, they will become float.
	start_R *= 1.0
	end_R   *= 1.0

	list = []
	Rs = frange(start_R, end_R, n)
	for R in Rs:
		list.append(R * cmath.exp(1j * theta))
	return list

# ----------------------------------------------------------------
# Example:  rnumint(sin, frange(0, 2*pi, 1000)).
# Again, this works fine for complexes as well.

# No adaptive quadrature -- just sums along the passed-in mesh.

def numint(f, xs):
	"""numint(f, xarray):  Naive numerical integration for float and complex."""
	sum = 0
	n = len(xs)
	ys = map(f, xs)
	for i in range(0, n-1):
		sum += 0.5 * (ys[i] + ys[i+1]) * (xs[i+1] - xs[i])
	sum += ys[n-1] * (xs[n-1]-xs[n-2])
	return sum

# ----------------------------------------------------------------
# Use the left-hand rule at the left endpoint, the right-hand rule at the
# right endpoint, and the midpoint rule at the interior points.
def numderiv(f, xs):
	"""numderiv(f, xarray):  Numerical differentiation."""
	n = len(xs)
	list = []

	# f'(x) ~= [ f(x+h) - f(x) ] / h
	x0 = xs[0]; x1 = xs[1]
	y0 = f(x0); y1 = f(x1)
	list.append((y1 - y0) / (x1 - x0))

	for i in range(1, n-1):
		# f'(x) ~= [ f(x+h) - f(x-h) ] / 2h
		x0 = xs[i-1]; x1 = xs[i+1]
		y0 = f(x0); y1 = f(x1)
		list.append((y1 - y0) / (x1 - x0))

	# f'(x) ~= [ f(x) - f(x-h) ] / h
	x0 = xs[n-2]; x1 = xs[n-1]
	y0 = f(x0); y1 = f(x1)
	list.append((y1 - y0) / (x1 - x0))
	return list

# ----------------------------------------------------------------
def clist_to_rlist(cs):
	list = []
	for c in cs:
		list.append(c.real)
		list.append(c.imag)
	return list
