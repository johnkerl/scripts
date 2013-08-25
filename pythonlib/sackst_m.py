#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import copy
import sys
import sni_gm
import fact_m
import sackmat_m

# ----------------------------------------------------------------
# To do:
# * Kronecker product representation?
# * Non-simple tensor class

# ----------------------------------------------------------------
def is_list(p):
	return type(p) == type([0])

# ----------------------------------------------------------------
def dims_of_list(T):
	dims = []
	p = T
	while (is_list(p)):
		dims.append(len(p))
		p = p[0]
	return dims

# ----------------------------------------------------------------
# For addition and subtraction
def check_dims_equal(A, B, func_name):
	da = dims_of_list(A)
	db = dims_of_list(B)
	if (da != db):
		print "%s: unequal dimensions %s and %s." % (func_name, str(da),
			str(db))
		sys.exit(1)
	return da

# ----------------------------------------------------------------
# For multiplication
def check_dims_all_equal(A, B, func_name):
	da = dims_of_list(A)
	db = dims_of_list(B)
	if (da == []):
		return []
	n = da[0]
	for i in da:
		for j in db:
			if (i != n) or (j != n):
				print "%s: unequal dimensions %s and %s." % (func_name,
					str(da), str(db))
				sys.exit(1)
	return n

# ----------------------------------------------------------------
def add_aux(A, B):
	check_dims_equal(A, B, "simple tensor add")
	if (not is_list(A)):
		return A + B
	C = []
	for i in range(0, len(A)):
		C.append(add_aux(A[i], B[i]))
	return C

# ----------------------------------------------------------------
def sub_aux(A, B):
	check_dims_equal(A, B, "simple tensor subtract")
	if (not is_list(A)):
		return A - B
	C = []
	for i in range(0, len(A)):
		C.append(sub_aux(A[i], B[i]))
	return C

# ----------------------------------------------------------------
def multidx(i, r, n):
	I = []
	for k in range(0, r):
		I.append(i % n)
		i = int(i / n)
	return I

# ----------------------------------------------------------------
class simple_tensor:

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def __init__(self, elements):
		self.elements = copy.deepcopy(elements)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def __getitem__(self, I):
		if (is_list(I)):
			p = self.elements
			for i in I:
				p = p[i]
			return p
		else:
			return self.elements[I]

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def __setitem__(self, I, value):
		if (is_list(I)):
			if (is_list(self.elements)):
				p = self.elements
				for i in I[0:-1]:
					p = p[i]
				p[I[-1]] = value
			else: # scalar
				self.elements = value
		else:
			self.elements[I] = value

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def dims(self):
		return dims_of_list(self.elements)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def product_of_dims(self):
		dims = self.dims()
		prod = 1
		for dim in dims:
			prod *= dim
		return prod

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def order(self):
		order = 0
		p = self.elements
		while (is_list(p)):
			order += 1
			p = p[0]
		return order

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def __add__(A, B):
		return simple_tensor(add_aux(A.elements, B.elements))

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def __sub__(A, B):
		return simple_tensor(sub_aux(A.elements, B.elements))

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def __mul__(A, B):
		n = check_dims_all_equal(A.elements, B.elements, "simple tensor mul")
		ra = A.order(); pa = A.product_of_dims()
		rb = B.order(); pb = B.product_of_dims()
		C = make_zero_simple_tensor(ra + rb, n)

		for ia in range(0, pa):
			I = multidx(ia, ra, n)
			for jb in range(0, pb):
				J = multidx(jb, rb, n)
				K = I + J  # Python list concatenation
				#print ">> C", K, "= A", I, "* B", J
				C[K] = A[I] * B[J]
		return C

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# Symmetric product:  compute the symmetrization of the tensor product.
	def __and__(A, B):
		C = A * B
		return C.Alt_or_Sym(0)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# Wedge product:  compute the alternation of the tensor product, then scale
	# by (k+l)!/k!l!.
	def __xor__(A, B):
		C = A * B
		C = C.Alt_or_Sym(1)

		k = A.order()
		l = B.order()
		p = C.product_of_dims()
		r = k + l
		n = len(C.elements[0])
		scale = fact_m.fact(k+l) / (1.0 * fact_m.fact(k) * fact_m.fact(l))

		for i in range(0, p):
			I = multidx(i, r, n)
			C[I] *= scale

		return C

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def str(self):
		pass

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def permute(self, sigma):
		# xxx what if scalar?
		n = len(self.elements[0])
		r = self.order()
		p = self.product_of_dims()
		C = make_zero_simple_tensor(r, n)
		for i in range(0, p):
			I = multidx(i, r, n)
			J = sigma.of(I)
			C[I] = self[J]
		return C

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def Alt_or_Sym(self, want_Alt):
		# xxx what if scalar?
		r = self.order()
		n = len(self.elements[0])
		p = self.product_of_dims()
		C = make_zero_simple_tensor(r,n)
		Sr = sni_gm.get_elements_str(r)
		for sigma in Sr:
			if (want_Alt and sigma.sgn() == -1):
				sign = -1
			else:
				sign = 1
			for i in range(0, p):
				I = multidx(i, r, n)
				J = sigma.of(I)
				C[I] += sign * self[J]
		scale = 1.0 / fact_m.fact(r)
		for i in range(0, p):
			I = multidx(i, r, n)
			C[I] *= scale
		return C

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def Alt(self):
		return self.Alt_or_Sym(1)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def Sym(self):
		return self.Alt_or_Sym(0)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# This is the apply method.
	#
	# T = sum_ijk T(e_i, e_j, e_k) e_i* x e_j* x e_k*
	#   = sum_ijk t_ijk e_i* x e_j* x e_k*
	# u = sum_r a_r e_r
	# v = sum_s a_s e_s
	# w = sum_t a_t e_t
	# T(u,v,w) = sum_ijk t_ijk e_i* x e_j* x e_k*(u, v, w)
	#   = sum_ijk t_ijk a_i b_j c_k
	def of(self, vectors):
		r = self.order()
		p = self.product_of_dims()
		if (r == 0):
			return self.elements
		n = len(self.elements)

		sum = 0
		for i in range(0, p):
			I = multidx(i, r, n)
			prod = self[I]
			for j in range(0, r):
				prod *= vectors[j][I[j]]
			sum += prod
		return sum

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# Transform the coordinates of the tensor, given a change-of-basis matrix.
	#
	# cov1:  g[j1]         = sum_{i1}         q[i1][j1]                     g[i1]
	# cov2:  g[j1][j2]     = sum_{i1, i2}     q[i1][j1] q[i2][j2]           g[i1][i2]
	# cov3:  g[j1][j2][j3] = sum_{i1, i2, i3} q[i1][j1] q[i2][j2] q[i3][j3] g[i1][i2][i3]

	def cob(self, Q, cov_flags):

		r = self.order()
		p = self.product_of_dims()
		if (r == 0):
			return self
		n = len(self.elements)

		# Invert Q only when necessary
		P = 0
		any_ctv = 0
		for f in cov_flags:
			if (f == 0):
				any_ctv = 1
		if (any_ctv):
			P = Q.inv()

		xform = make_zero_simple_tensor(r, n)
		for j in range(0, p):
			J = multidx(j, r, n)
			sum = 0.0
			for i in range(0, p):
				I = multidx(i, r, n)
				prod = self[I]
				for k in range(0, r):
					if (cov_flags[k]):
						prod *= Q[I[k]][J[k]]
					else:
						prod *= P[J[k]][I[k]]
				sum += prod
			xform[J] = sum
		return xform

	def cov_cob(self, Q):
		r = self.order()
		cov_flags = [1] * r
		return self.cob(Q, cov_flags)

	def ctv_cob(self, Q):
		r = self.order()
		cov_flags = [0] * r
		return self.cob(Q, cov_flags)

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def printf(self, format="%7.4f"):
		r = self.order()
		dims = self.dims()
		if (r == 0):
			print format % (self.elements)
		if (r == 1):
			for i in range(0, dims[0]):
				print format % (self.elements[i]),
			print
			print
		elif (r == 2):
			# i selects the row
			# j selects the column
			for i in range(0, dims[0]):
				for j in range(0, dims[1]):
					print format % (self.elements[i][j]),
				print
			print
		elif (r == 3):
			# i selects the face
			# j selects the row
			# k selects the column
			for j in range(0, dims[1]):
				for i in range(0, dims[0]):
					for k in range(0, dims[2]):
						print format % (self.elements[i][j][k]),
					print " ",
				print
			print
		elif (r == 4):
			for i in range(0, dims[0]):
				for k in range(0, dims[2]):
					for j in range(0, dims[1]):
						for l in range(0, dims[3]):
							print format % (self.elements[i][j][k][l]),
						print " ",
					print
				print
			print
		else:
			print self.elements # Python list output

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	def dump(self):
		print "ordr = ",; print self.order()
		print "dims = ",; print self.dims()
		print "body = ",; print self.elements
		print

# ----------------------------------------------------------------
def make_zero_simple_tensor(r, n):
	if (r < 0):
		print "make_zero_simple_tensor:  invalid order %d." % (r)
		sys.exit(1)
	elif (r == 0):
		return simple_tensor(0)
	elif (r == 1):
		Z = [0] * n;
		return simple_tensor(Z)
	else:
		Z0 = make_zero_simple_tensor(r-1, n)
		Z1 = []
		for i in range(0, n):
			Z1.append(copy.deepcopy(Z0.elements))
		return simple_tensor(Z1)

# ----------------------------------------------------------------
def make_ones_simple_tensor(r, n):
	if (r < 0):
		print "make_ones_simple_tensor:  invalid order %d." % (r)
		sys.exit(1)
	elif (r == 0):
		return simple_tensor(1)
	elif (r == 1):
		Z = [1] * n;
		return simple_tensor(Z)
	else:
		Z0 = make_ones_simple_tensor(r-1, n)
		Z1 = []
		for i in range(0, n):
			Z1.append(copy.deepcopy(Z0.elements))
		return simple_tensor(Z1)

# ----------------------------------------------------------------
def make_I_simple_tensor(r, n):
	A = make_zero_simple_tensor(r, n)
	if (r == 0):
		A.elements = 1
	else:
		for i in range(0, n):
			I = [i] * r
			A[I] = 1
	return A
