#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# See the Wikipedia article on Autoregressive_model.
# kerl.john.r@gmail.com
# 2010-11-16
# ================================================================

import sys, random, copy

# AR(p) process:
# X[i] = c + sum_{j=1}^p a[j] X[i-j] + eps[i]
# where eps[i] ~ N(0, sigma_eps^2)
# ... perhaps eps[i] with non-normal distributions also could be used to create
# something called AR(p)?

class ARp_t:
	# c_and_as:  [c    a[1]   a[2]   ... a[p]]
	# X_i_minus: [X[i] X[i-1] X[i-2] ... X[i-p]]
	def __init__(self, c_and_as, sigma_eps):
		self.p = len(c_and_as) - 1
		self.i = 0
		if self.p < 1:
			print >> sys.stderr, "Need at least c and one a."
			print >> sys.stderr, "Pass a1=0 to get no a's."
			sys.exit(1)
		self.c_and_as = c_and_as
		self.sigma_eps = sigma_eps
		self.X_i_minus = [0] * (self.p+1)
		self.js_1_to_p = range(1, self.p+1)
		self.js_pm1_to_0 = range(self.p-1, -1, -1)

	# E.g. with p=2:
	# X[i-2] = X[i-1]
	# X[i-1] = X[i]
	# X[i] = c + a[1]*X[i-1] + a[2]*X[i-2]
	def update(self):
		for j in self.js_pm1_to_0:
			self.X_i_minus[j+1] = self.X_i_minus[j]
		Xi = self.c_and_as[0] # c
		for j in self.js_1_to_p:
			Xi += self.c_and_as[j] * self.X_i_minus[j]
		Xi += random.gauss(0, self.sigma_eps)
		self.X_i_minus[0] = Xi
		self.i += 1

	def get(self):
		return self.X_i_minus[0]

	def get_and_update(self):
		Xi = self.X_i_minus[0]
		self.update()
		return Xi

	def get_all(self):
		#return copy.copy(self.X_i_minus)
		return self.X_i_minus

	def __str__(self):
		string = 'i=%d p=%d (c=%.4f' % (self.i, self.p, self.c_and_as[0])
		for j in self.js_1_to_p:
			string += ' a[%d]=%.4f' % (j, self.c_and_as[j])
		string += ')'
		for j in range(0, self.p+1):
			string += ' X[%d]=%.4f' % (self.i-j, self.X_i_minus[j])
		return string

	def __repr__(self):
		return __str__(self)

# ----------------------------------------------------------------
def usage():
	print >> sys.stderr, "Usage: %s {n}" % (sys.argv[0])
	print >> sys.stderr, "Or:    %s {n} {nA}" % (sys.argv[0])
	print >> sys.stderr, "Or:    %s {n} {nA} {c} {a1 a2 ...}" % (sys.argv[0])
	sys.exit(1)

# ----------------------------------------------------------------
# N.B.:
# * c=0  a1=1 a2=1 sigma=0:  fibo
# * c=1  a1=1      sigma=0: counter
# * c=mu a1=0      sigma=1: IID N(mu, sigma)

n = 20
nA = 10
c_and_as = [0, 0.999]
sigma_eps = 1

argc = len(sys.argv)
if argc == 1:
	pass
elif argc == 2:
	if sys.argv[1] == '-h' or sys.argv[1] == '--help':
		usage()
	n = int(sys.argv[1])
elif argc == 3:
	n = int(sys.argv[1])
	nA = int(sys.argv[2])
elif argc >= 5:
	n = int(sys.argv[1])
	nA = int(sys.argv[2])
	c_and_as = map(float, sys.argv[3:])
else:
	usage()

ARps = [0] * nA
for j in range(0, nA):
	ARps[j] = ARp_t(c_and_as, sigma_eps)
for i in range(0, n):
	for j in range(0, nA):
		print ARps[j].get_and_update(),
	print
