#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2005-11-07
#
# This is a Python library for simple I/O and arithmetic on vectors
# and matrices of floating-point numbers.
#
# Why not use packages such as Numpy?  Sometimes, I prefer to have a small,
# simple set of routines which I wrote and completely understand, which do no
# more and no less than what I want them to do.  For black-box linear-algebra
# software, you're better off with Matlab, Numpy, etc.  The code here is of a
# different sort:  simple and simple-minded, and intended to be not just used
# but also read.
#
# ================================================================

# ================================================================
from __future__ import division # 1/2 = 0.5, not 0.
import sys
import copy
import re
import math
import array # For binary I/O
import types
from cplxreal_m import *

# ----------------------------------------------------------------
def frac_reader(s):
	pieces = re.split(r'/', s, 2)
	if len(pieces) == 2:
		return float(pieces[0]) / float(pieces[1])
	else:
		return float(s)

# ----------------------------------------------------------------
# A keystroke-saver for the matrix constructor.
def m(list):
	return sackmat(list)

# ----------------------------------------------------------------
def sm_is_list(p):
	return type(p) == type([0])

# ----------------------------------------------------------------
def check_same_matrix_dims(A, B, func_name):
	# To do: check is-list twice
	[anr, anc] = A.dims()
	[bnr, bnc] = B.dims()
	if (anr != bnr) or (anc != bnc):
		print >> sys.stderr, "%s: mismatched lengths %dx%d, %dx%d." \
			% (func_name, anr, anc, bnr, bnc)
		sys.exit(1)
	return [anr, anc]

# ----------------------------------------------------------------
def check_mul_matrix_dims(A, B, func_name):
	# To do: check is-list x 4
	[anr, anc] = A.dims()
	[bnr, bnc] = B.dims()
	if (anc != bnr):
		print >> sys.stderr, "%s: mismatched mul lengths %dx%d, %dx%d." % (func_name, anr, anc, bnr, bnc)
		sys.exit(1)
	return [anr, anc, bnr, bnc]

# ----------------------------------------------------------------
# Use the metric induced by the max norm.
def are_close_in_max_norm(A, B, tol = 1e-10):
	[nr, nc] = check_same_matrix_dims(A, B, "sackmat are_close_in_max_norm")
	for i in range(0, nr):
		for j in range(0, nc):
			d = abs(A[i][j] - B[i][j])
			if (d > tol):
				return 0
	return 1

# ----------------------------------------------------------------
def make_zero_matrix(nr, nc):
	row = [0] * nc
	elts = []
	for i in range(0, nr):
		elts.append(copy.copy(row))
	return sackmat(elts)

# ----------------------------------------------------------------
def make_identity_matrix(n):
	I = make_zero_matrix(n, n)
	for i in range(0, n):
		I[i][i] = 1
	return I

# ----------------------------------------------------------------
# This is simply a test pattern.
# 1 2 3
# 4 5 6
# 7 8 9

def make_seq_matrix(nr, nc):
	A = make_zero_matrix(nr, nc)
	k = 0
	for i in range(0, nr):
		for j in range(0, nc):
			k += 1
			A[i][j] = k
	return A

# Same, except non-singular.
def make_nseq_matrix(nr, nc):
	A = make_zero_matrix(nr, nc)
	k = 0
	for i in range(0, nr):
		for j in range(0, nc):
			k += 1
			if (i == j):
				A[i][j] = -k
			else:
				A[i][j] =  k
	return A

# ----------------------------------------------------------------
def matrix_times_vector(A, v):
	Av = []
	[nr, nc] = A.dims()
	n = len(v)
	for i in range(0, nr):
		Av.append(vecdot(A[i], v))
	return Av

# ----------------------------------------------------------------
def vector_times_matrix_times_vector(u, A, v):
	return vecdot(u, matrix_times_vector(A, v))

# ----------------------------------------------------------------
def vecadd(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecadd")
	n = len(u)
	w = []
	for i in range(0, n):
		w.append(u[i] + v[i])
	return w

# ----------------------------------------------------------------
def vecaddip(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecadd")
	n = len(u)
	for i in range(0, n):
		u[i] += v[i]

# ----------------------------------------------------------------
def vecsadd(u, v, s):
	#n = check_same_list_dims(u, v, "sackmat vecadd")
	n = len(u)
	w = []
	for i in range(0, n ):
		w.append(u[i] + s*v[i])
	return w

# ----------------------------------------------------------------
def vecsaddip(u, v, s):
	#n = check_same_list_dims(u, v, "sackmat vecadd")
	n = len(u)
	for i in range(0, n):
		u[i] += s*v[i]

# ----------------------------------------------------------------
def vecsub(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecsub")
	n = len(u)
	w = []
	for i in range(0, n):
		w.append(u[i] - v[i])
	return w

# ----------------------------------------------------------------
def vecmul(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecsub")
	n = len(u)
	w = []
	for i in range(0, n):
		w.append(u[i] * v[i])
	return w

# ----------------------------------------------------------------
def vecdiv(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecsub")
	n = len(u)
	w = []
	for i in range(0, n):
		w.append(u[i] / v[i])
	return w

# ----------------------------------------------------------------
def vecssub(u, v, s):
	#n = check_same_list_dims(u, v, "sackmat vecsub")
	n = len(u)
	w = []
	for i in range(0, n ):
		w.append(u[i] - s*v[i])
	return w

# ----------------------------------------------------------------
def vecdot(u, v):
	s = 0
	n = len(u)
	#n = check_same_list_dims(u, v, "sackmat vecdot")
	for i in range(0, n):
		s += u[i] * v[i]
	return s

# ----------------------------------------------------------------
def vecpair(u, v):
	s = 0
	n = len(u)
	#n = check_same_list_dims(u, v, "sackmat vecdot")
	for i in range(0, n):
		ui = u[i]
		s += u[i] * v[i]
	return s

# ----------------------------------------------------------------
def outer(u, v):
	m = len(u)
	n = len(v)
	uv = make_zero_matrix(m, n)
	for i in range(0, m):
		for j in range(0, n):
			uv[i][j] = u[i] * v[j]
	return uv

# ----------------------------------------------------------------
def outer1(u):
	return outer(u, u)

# ----------------------------------------------------------------
def vecnorm(u):
	return math.sqrt(vecdot(u, u))
def vecnormsq(u):
	return vecdot(u, u)
def normalize(u):
	return vecsmul(u, 1.0 / vecnorm(u))

# ----------------------------------------------------------------
def vecsmul(u, s):
	v = []
	for ue in u:
		v.append(ue * s)
	return v

# ----------------------------------------------------------------
def vecsdiv(u, d):
	v = []
	for ue in u:
		v.append(ue / d)
	return v

# ----------------------------------------------------------------
def vechat(u):
	return vecsmul(u, 1.0/vecnorm(u))

# ----------------------------------------------------------------
def vec_contract(u):
	sum = 0.0
	n = len(u)
	for i in range(0, n):
		sum += u[i]
	return sum

# ----------------------------------------------------------------
def print_row_vector(v, format="%11.7f"):
	n = len(v)
	for i in range(0, n):
		print format % (v[i]),
	print

def print_row_vector_no_cr(v, format="%11.7f"):
	n = len(v)
	for i in range(0, n):
		print format % (v[i]),

def print_row_vectors(vs, format="%11.7f"):
	nv = len(vs)
	for j in range(0, nv):
		print_row_vector(vs[j])

# ----------------------------------------------------------------
def print_column_vector(v, format="%11.7f"):
	n = len(v)
	for i in range(0, n):
		print format % (v[i])

def print_column_vector_to_file(v, file_name, format="%11.7f"):
	if (file_name == "-"):
		file_handle = sys.stdout
	else:
		try:
			file_handle = open(file_name, 'w')
		except:
			print >> sys.stderr, \
				"Couldn't open \"" + file_name + "\" for write."
			sys.exit(1)


	n = len(v)
	for i in range(0, n):
		string = format % (v[i])
		file_handle.write(string)
		file_handle.write('\n')

	if (file_name != "-"):
		file_handle.close()

# ----------------------------------------------------------------
def row_vector_from_string(orig_line, elt_scanner):
	v = []
	line = copy.copy(orig_line)

	if line == '':
		return v
	# Chomp trailing newline, if any.
	if line[-1] == '\n':
		line = line[0:-1]

	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	if line == '':
		return v

	# Tokenize.
	strings = re.split(r"\s+", line)

	# Scan.  Try exception?
	for s in strings:
		elt = elt_scanner(s)
		v.append(elt)

	return v

# ----------------------------------------------------------------
def read_row_vector(elt_scanner, file_name = "-"):
	v = []

	if file_name == '-':
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	# Note that "for line in sys.stdin" slurps *all* the input.
	# We may not want all of it.
	line = ""
	while (line == ""):
		line = file_handle.readline()

	v = row_vector_from_string(line, elt_scanner)
	if v == []:
		print >> sys.stderr, "sackmat read_row_vector: empty input."
		sys.exit(1)

	if file_name != '-':
		file_handle.close()

	return v

# ----------------------------------------------------------------
def read_column_vector(elt_scanner, file_name = "-"):
	v = []

	if file_name == '-':
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	# Note that "for line in sys.stdin" slurps *all* the input.
	# We may not want all of it.
	while (1):
		line = file_handle.readline()
		if line == '':
			break

		# Strip comments.
		line = re.sub(r"#.*",  r"", line)
		# Strip leading and trailing whitespace.
		line = re.sub(r"^\s+", r"", line)
		line = re.sub(r"\s+$", r"", line)
		# Skip blank lines.
		if re.match(r"^$", line):
			continue

		elt = elt_scanner(line)
		v.append(elt)

	if file_name != '-':
		file_handle.close()

	return v

# ----------------------------------------------------------------
# Standard basis vector.
def stdbv(i, n):
	ei = [0] * n
	ei[i] = 1
	return ei

# ----------------------------------------------------------------
# Utility routine for row reduction
# Return value:  True/false (if index was found), and index

def find_leader_pos(v, tol=1e-7):
	n = len(v)
	for j in range(0, n):
		if abs(v[j]) >= tol:
			return [1, j]
	return [0, 0]

def tol_zero(x, tol=1e-7):
	if abs(x) < tol:
		return 1
	else:
		return 0

# ----------------------------------------------------------------
def vector_is_zero(v, tol=1e-7):
	n = len(v)
	for i in range(0, n):
		if not tol_zero(v[i]):
			return 0
	return 1

# ----------------------------------------------------------------
# projpar:  Returns the component of u which is parallel to a.
# projperp: Returns the component of u which is perpendicular to a.
#
# * u = u_par + u_perp where the former is parallel to a and the latter
#   is perpendicular.
# * Thus u_perp = u - u_par
# * u_par has magnitude ||u|| cos theta, and direction a.
# * u dot a is ||u|| ||a|| cos theta
# * u_par = ||u|| cos theta a^hat
#         = ||u|| cos theta a / ||a||
#         = (u dot a) a / ||a||^2
#         = (u dot a) a / (a dot a)
#   which is a familiar construction from the Gram-Schmidt process.

def projpar(u, a):
	n = len(u)
	ua = vecdot(u, a)
	aa = vecdot(a, a) # To do: needs divide-by-zero check
	# The cast to float is in case the inputs are integers.
	u_par = vecsmul(a, float(ua)/float(aa))
	return u_par

def projperp(u, a):
	u_par = projpar(u, a)
	u_perp = vecsub(u, u_par)
	return u_perp

# ----------------------------------------------------------------
# Pastes column vectors into a matrix.
# Example:
#
# u = [1] v = [3] w = [5]
#     [2]     [4]     [6]
#
# A = [1 3 5]
#     [2 4 6]
#
# Sample syntax:
# A = sackmat_m.paste_column_vectors([[1, 2], [3, 4], [5, 6]])

def paste_column_vectors(vectors):
	nr = len(vectors[0])
	nc = len(vectors)
	A  = make_zero_matrix(nr, nc)
	for i in range(0, nr):
		for j in range(0, nc):
			A[i][j] = vectors[j][i]
	return A

# ----------------------------------------------------------------
# Pastes row vectors into a matrix.
# Example:
#
# u = [1 2]
# v = [3 4]
# w = [5 6]
#
#     [1 2]
# A = [3 4]
#     [5 6]
#
# Sample syntax:
# A = sackmat_m.paste_row_vectors([[1, 2], [3, 4], [5, 6]])

def paste_row_vectors(vectors):
	nr = len(vectors)
	nc = len(vectors[0])
	A  = make_zero_matrix(nr, nc)
	for i in range(0, nr):
		for j in range(0, nc):
			A[i][j] = vectors[i][j]
	return A

# ----------------------------------------------------------------
# basis_coeffs():
# Coefficients of v with respect to a basis, in the general case.
#
# Example:
#
# v = [3] <---- Input vector
#     [4]
#
# u1 = [ 1]   u2 = [1] <---- Basis vectors
#      [-1]        [2]
#
# v = a[ 1] + b[1]  <---- a, b are the coefficients to be determined.
#      [-1]    [2]
#
#   =  [ a] +  [b]  =  [ a +  b]  =  [ 1  1] [a]  =  [u1 | u2] [a]
#      [-a]   [2b]     [-a + 2b]     [-1  2] [b]               [b]
#
# so
#
# [a] = [u1 | u2]^-1  v  = [ 1 |  1]^-1  [3]
# [b]                      [-1 |  2]     [4]
#
#     = [2/3 | -1/3]  [3]  = [2/3]
#       [1/3 |  1/3]  [4]    [7/3]
#
# Check:
#
#   2/3[ 1] + 7/3[1]  = [ 2/3] + [ 7/3]  = [3]  = v.
#      [-1]      [2]    [-2/3]   [14/3]    [4] 
#
# Sample syntax:
#   basis = [[1, -1], [1, 2]]
#   v = [3, 4]
#   c = sackmat_m.basis_coeffs(v, basis)
# which results in 
#   v =  [3, 4]
#   c =  [0.66666666666666652, 2.333333333333333]

def basis_coeffs(v, basis):
	A = paste_column_vectors(basis)
	Ai = A.inv()
	return Ai * v

# ----------------------------------------------------------------
# basis_coeffs_on():
# Coefficients of v with respect to an orthonormal basis.
#
# An arbitrary vector v is
#
#   v = sum_{j=1}^N c_j u_j
#
# but dot with u_i:
#
#   <u_i, v> = <u_i, sum_{j=1}^N c_j u_j>
#            = sum_{j=1}^N c_j <u_i, u_j>
#            = sum_{j=1}^N c_j delta_ij
#            = c_i
#
# i.e. c_i = <u_i, v>.

def basis_coeffs_on(v, basis):
	n = len(basis[0])
	coeffs = []
	for j in range(0, n):
		coeffs.append(vecdot(basis[j], v))
	return coeffs

# ----------------------------------------------------------------
# Sample syntax:
#   u = sackmat_m.linear_combination([2, 3],    [[1,0,0],[0,0,1]])
#   v = sackmat_m.linear_combination([2, 3, 4], [[1,0],[0,1],[100,200]])
# which results in
#   u =  [2.0, 0.0, 3.0]
#   v =  [402.0, 803.0]

def linear_combination(coeffs, vectors):
	n = len(vectors[0])
	v = [0.0] * n
	nvec = len(vectors)
	for veci in range(0, nvec):
		for eltj in range(0, n):
			v[eltj] += coeffs[veci] * vectors[veci][eltj]
	return v

# ----------------------------------------------------------------
# Q = I - 2 v v^t / (v^t v)
#
# Reflection matrices have determinant -1.  However, if v is the zero vector
# (or nearly so), the best we can do is to hand back the identity matrix, which
# has determinant +1.  The return value is that sign.

def householder_vector_to_Q(v):
	# To do: package the tol ...
	tol = 1e-10
	n = len(v)
	v_dot_v = vecdot(v, v)
	Q = make_identity_matrix(n)
	sign = 1
	if v_dot_v >= tol:
		two_over_v_dot_v = 2.0 / v_dot_v
		for i in range(0, n):
			for j in range(0, n):
				Q[i][j] -= v[i]*v[j] * two_over_v_dot_v
		sign = -1
	return [Q, sign]

# ----------------------------------------------------------------
def validate_matrix(A, func_name):
	#To do: is-list A -- put into sackutil
	nr = len(A)
	if nr < 1:
		print >> sys.stderr, func_name + ":  no rows."
		sys.exit(1)
	nc = len(A[0])
	if nc < 1:
		print >> sys.stderr, func_name + ":  empty row."
		sys.exit(1)
	for row in A:
		if len(row) != nc:
			print >> sys.stderr, func_name + ":  ragged input."
			sys.exit(1)
	return [nr, nc]

# ================================================================
class sackmat:

	def __init__(self, elements):
		# To do: validate non-ragged
		self.elements = copy.deepcopy(elements)

	def dims(self):
		return [len(self.elements), len(self.elements[0])]
	def square_dim(self):
		[nr, nc] = self.dims()
		if nr != nc:
			print >> sys.stderr, "Non-square input."
			sys.exit(1)
		return nr

	def num_rows(self):
		return len(self.elements)
	def num_cols(self):
		return len(self.elements[0])

	def fill_zero_matrix(self):
		[nr, nc] = self.dims()
		for i in range(0, nr):
			for j in range(0, nc):
				self.elements[i][j] = 0.0
	def fill_identity_matrix(self):
		n = self.square_dim()
		for i in range(0, n):
			for j in range(0, n):
				self.elements[i][j] = 0.0
		for i in range(0, n):
			self.elements[i][i] = 1.0

	def __getitem__(self, i):
		return self.elements[i]

	def __setitem__(self, i, value):
		self.elements[i] = value

	def __add__(A, B):
		[nr, nc] = check_same_matrix_dims(A, B, "sackmat add")
		C = make_zero_matrix(nr, nc)
		for i in range(0, nr):
			for j in range(0, nc):
				C[i][j] = A[i][j] + B[i][j]
		return C

	def __sub__(A, B):
		[nr, nc] = check_same_matrix_dims(A, B, "sackmat sub")
		C = make_zero_matrix(nr, nc)
		for i in range(0, nr):
			for j in range(0, nc):
				C[i][j] = A[i][j] - B[i][j]
		return C

	# We can get here via matrix times something, i.e. A*B where A is a matrix.
	# B can be whatever, but currently I support only B being a matrix (sackmat
	# object), vector (list), or scalar.
	# 
	# A Python implementation detail:  If one puts the scalar on the left, e.g.
	# 2.0 * A, we won't even get called here.
	def __mul__(A, B):
		B_is_matrix = 1
		try:
			x = B.elements
		except:
			B_is_matrix = 0

		if B_is_matrix:
			[anr, anc, bnr, bnc] = check_mul_matrix_dims(A, B, "sackmat mul")
			C = make_zero_matrix(anr, bnc)
			for i in range(0, anr):
				for j in range(0, bnc):
					C[i][j] = 0
					for k in range(0, anc):
						C[i][j] += A[i][k] * B[k][j]
			return C
		elif sm_is_list(B):
			return matrix_times_vector(A, B)
		else:
			[anr, anc] = A.dims()
			C = make_zero_matrix(anr, anc)
			for i in range(0, anr):
				for j in range(0, anc):
					C[i][j] = A[i][j] * B
			return C

	def __neg__(A):
		[nr, nc] = A.dims()
		C = make_zero_matrix(nr, nc)
		for i in range(0, nr):
			for j in range(0, nc):
				C[i][j] = -A[i][j]
		return C

	def __pow__(A, n):
		if type(n) != type(1):
			print >> sys.stderr, \
				"sackmat __pow__:  exponent <<", n, ">> is non-integer."
			sys.exit(1)

		if n < 0:
			Ap = A.inv()
			n = -n
		elif n == 0:
			return A*A.inv()
		else:
			Ap = copy.deepcopy(A)

		A2 = Ap
		n -= 1
		while (n > 0):
			if n & 1:
				Ap = Ap * A2
			n = n >> 1
			A2 = A2 * A2
		return Ap

	# Overload the % operator for Kronecker product.
	def __mod__(A, B):
		return kronecker_product(A, B)

	def copy_elements_from(self, other):
		check_same_matrix_dims(self, other, "copy_elements_from")
		[nr, nc] = self.dims()
		for i in range(0, nr):
			for j in range(0, nc):
				self.elements[i][j] = other.elements[i][j]

	def copy_elements_to(self, other):
		check_same_matrix_dims(self, other, "copy_elements_to")
		[nr, nc] = self.dims()
		for i in range(0, nr):
			for j in range(0, nc):
				other.elements[i][j] = self.elements[i][j]

	def smul(self, s):
		[nr, nc] = self.dims()
		C = make_zero_matrix(nr, nc)
		for i in range(0, nr):
			for j in range(0, nc):
				C[i][j] = s * self.elements[i][j]
		return C

	def smul_in_place(self, s):
		[nr, nc] = self.dims()
		for i in range(0, nr):
			for j in range(0, nc):
				self.elements[i][j] = s * self.elements[i][j]

	def to_scalar(self):
		[nr, nc] = self.dims()
		if (nr != 1 or nc != 1):
			print >> sys.stderr, \
				"sackmat to_scalar: input dimensions must be 1x1; got %dx%d." \
				% (nr, nc)
			sys.exit(1)
		# Also try to hande the case when it's bigger than 1x1, but
		# is a scalar multiple of the identity (to within a tolerance).
		return self.elements[0][0]

	def transpose(self):
		[nr, nc] = self.dims()
		C = make_zero_matrix(nc, nr)
		for i in range(0, nr):
			for j in range(0, nc):
				C[j][i] = self.elements[i][j]
		return C

	def conjugate_transpose(self):
		[nr, nc] = self.dims()
		C = make_zero_matrix(nc, nr)
		for i in range(0, nr):
			for j in range(0, nc):
				C[j][i] = conj(self.elements[i][j])
		return C
	def star(self):
		return self.conjugate_transpose()

	#    0 1 2 3 4 5
	# 0  . . . . . .
	# 1  o . . . . .
	# 2  o o . . . .
	# 3  o o o . . .
	# 4  o o o o . .
	# 5  o o o o o .
	def transpose_in_place(self):
		n = self.square_dim()
		for i in range(0, n):
			for j in range(0, i):
				temp                = self.elements[i][j]
				self.elements[i][j] = self.elements[j][i]
				self.elements[j][i] = temp

	def A_star_A(self):
		n = self.square_dim()
		C = make_zero_matrix(n, n)
		for i in range(0, n):
			for j in range(0, n):
				C[i][j] = 0.0
				for k in range(0, n):
					C[i][j] += conj(self.elements[k][i]) * self.elements[k][j]
		return C

	def __str__(self):
		[nr, nc] = self.dims()
		mat_string = ""
		for i in range(0, nr):
			row_string = str(self.elements[i][0])
			for j in range(1, nc):
				row_string += " " + str(self.elements[i][j])
			mat_string += row_string + "\n"
		return mat_string

	def __repr__(self):
		return self.__str__()

	def printp(self, name, format="%11.7f"):
		print "%s:" % (name)
		self.printf(format)
		print

	def printf(self, format="%11.7f"):
		[nr, nc] = self.dims()
		if isinstance(self.elements[0][0], complex):
			# This is a hack -- hard-coding %.6f for the imaginary part.  I
			# want complexes printed without any embedded whitespace, so that
			# my reader routine can naively isolate matrix elements by looking
			# at whitespace.
			cpformat = format + "+" + "%.6fj"
			cnformat = format + "-" + "%.6fj"
			for i in range(0, nr):
				for j in range(0, nc):
					rr = self.elements[i][j].real
					ii = self.elements[i][j].imag

					#print format % (rr),
					#print format % (ii),

					# Use abs to handle the fact that IEEE floating-point has
					# signed zero.  I don't want to be printing "3+-0j" when
					# printing a conjugated real.
					if (ii < 0.0):
						print cnformat % (rr, abs(ii)),
					else:
						print cpformat % (rr, abs(ii)),
				print
		else:
			for i in range(0, nr):
				for j in range(0, nc):
					print format % (self.elements[i][j]),
				print
		return

	def get_submatrix_column(self, colidx, start_row):
		[nr, nc] = self.dims()
		submatrix_column = []
		for src in range(start_row, nr):
			submatrix_column.append(self.elements[src][colidx])
		return submatrix_column

	def put_submatrix_column(self, colidx, start_row, column):
		[nr, nc] = self.dims()
		src = 0
		for dst in range(start_row, nr):
			self.elements[dst][colidx] = column[src]
			src += 1
		return

	# ----------------------------------------------------------------
	# Example:
	# Let A be 6 x 8 and Q be 4 x 4.
	# Start at row 3, column 3 of A.

	# Q: [1          ]  A: [. . . . . . . .]
	#    [  1        ]     [. . . . . . . .]
	#    [    o o o o]     [. . o o o o o o]
	#    [    o o o o]     [. . o o o o o o]
	#    [    o o o o]     [. . o o o o o o]
	#    [    o o o o]     [. . o o o o o o]

	# The 1's are virtual; if Q *were* 6x6, the 1's were 1's, and the blanks
	# were 0's, then the same product would be obtained (at the cost of more
	# arithmetic operations).

	# tmp                      sub                 self
	#                                                    j ------>
	# Q*A: [               ]   Q: [1            ]  A: k [. . . . . . . .]
	#      [    j ---->    ]      [  1 k ---->  ]     | [. . . . . . . .]
	#      [  i # o o o o o]      [  i # # # #  ]     | [. . # o o o o o]
	#      [  | o o o o o o]      [  | o o o o  ]     v [. . # o o o o o]
	#      [  | o o o o o o]      [  | o o o o  ]       [. . # o o o o o]
	#      [  v o o o o o o]      [  v o o o o  ]       [. . # o o o o o]
	#      [               ]      [            1]       [. . . . . . . .]

	# tmp                      sub                 self
	#                                                    j ------>
	# Q*A: [               ]   Q: [1            ]  A: k [. . . . . . . .]
	#      [j ---->        ]      [  1 k----->  ]     | [. . . . . . . .]
	#    i [o o # o o o o o]      [  i # # # #  ]     | [o o # o o o o o]
	#    | [o o o o o o o o]      [  | o o o o  ]     v [o o # o o o o o]
	#    | [o o o o o o o o]      [  | o o o o  ]       [o o # o o o o o]
	#    v [o o o o o o o o]      [  v o o o o  ]       [o o # o o o o o]
	#      [               ]      [            1]       [. . . . . . . .]

	# To do: doc self_start_col:  for when previous columns are already known to be zero.

	def premultiply_by_submatrix(self, sub, sub_start_row, self_start_col):
		[self_nr, self_nc] = self.dims()
		[sub_nr, sub_nc]   = sub.dims()
		[tmp_nr, tmp_nc]   = [sub_nr, self_nc - self_start_col]
		tmp = make_zero_matrix(tmp_nr, tmp_nc)

		# First, form the product out of place.
		# C[i][j] = sum_k A[i][k] B[k][j]
		for tmpi in range(0, tmp_nr):
			subi = tmpi
			for tmpj in range(0, tmp_nc):
				selfj = tmpj + self_start_col
				value = 0.0
				for subk in range(0, sub_nc):
					selfk = sub_start_row + subk
					value += sub.elements[subi][subk] * self.elements[selfk][selfj]
				tmp[tmpi][tmpj] = value

		# Second, copy the product back in place.
		for tmpi in range(0, tmp_nr):
			selfi = tmpi + sub_start_row
			for tmpj in range(0, tmp_nc):
				selfj = tmpj + self_start_col
				self.elements[selfi][selfj] = tmp.elements[tmpi][tmpj]

	# ----------------------------------------------------------------
	# To do: port me from premul:  this is just a stub.

	# tmp                   self                 sub
	#             j ---->         k ---->
	# A*Q^t: [  i # o o o]  A: i [. . # # # #]   Q: [1          ]
	#        [  | o o o o]     | [. . o o o o]      [  1 k ---->]
	#        [  | o o o o]     | [. . o o o o]      [  j # # # #]
	#        [  v o o o o]     v [. . o o o o]      [  | o o o o]
	#        [    o o o o]       [. . o o o o]      [  | o o o o]
	#        [    o o o o]       [. . o o o o]      [  v o o o o]

	def postmultiply_by_submatrix_transpose(self, sub, sub_start_col):
		[self_nr, self_nc] = self.dims()
		[sub_nr, sub_nc]   = sub.dims()
		[tmp_nr, tmp_nc]   = [self_nr, sub_nc]
		tmp = make_zero_matrix(tmp_nr, tmp_nc)

		# First, form the product out of place.
		# C[i][j] = sum_k A[i][k] B[j][k]
		for tmpi in range(0, tmp_nr):
			selfi = tmpi
			for tmpj in range(0, tmp_nc):
				subj = tmpj
				value = 0.0
				for subk in range(0, sub_nc):
					selfk = sub_start_col + subk
					value += self.elements[selfi][selfk] * sub.elements[subj][subk] 
				tmp[tmpi][tmpj] = value

		# Second, copy the product back in place.
		for tmpi in range(0, tmp_nr):
			selfi = tmpi
			for tmpj in range(0, tmp_nc):
				selfj = tmpj + sub_start_col
				self.elements[selfi][selfj] = tmp.elements[tmpi][tmpj]

	# ----------------------------------------------------------------
	# This assumes submatrices begin on diagonal elements.
	# o o o o o o
	# . o o o o o
	# . . o o o o
	# . . . o o o
	# . . . . o o
	# . . . . . o

	def householder_UT_pass_on_submatrix(self, submxidx, tol = 1e-5, arg_Q = 0.0):
		[nr, nc] = self.dims()
		height = nr - submxidx

		# Get the 1st column of the submatrix
		u = self.get_submatrix_column(submxidx, submxidx)

		# Compute ||u|| and v.
		v0 = math.sqrt(vecdot(u, u))
		if (u[0] >= 0):
			v0 = -v0
		v = [0] * height
		v[0] = v0

		# Compute axis = u - v.
		axis = vecsub(u, v)

		# Compute the Householder transformation.
		[Q, sign] = householder_vector_to_Q(axis)

		# Apply the Householder transformation.
		# Example:
		# Let A be 6 x 8.
		# Start at row 3, column 3 of A.
		# Then Q is 4 x 4:
		#
		# Q: [1          ]  A: [. . . . . . . .]
		#    [  1        ]     [. . . . . . . .]
		#    [    o o o o]     [. . o o o o o o]
		#    [    o o o o]     [. . o o o o o o]
		#    [    o o o o]     [. . o o o o o o]
		#    [    o o o o]     [. . o o o o o o]

		self.premultiply_by_submatrix(Q, submxidx, submxidx)

		# If they want an updated version of the Q matrix, give it back to
		# them.
		if (not isinstance(arg_Q, float)):
			arg_Q.premultiply_by_submatrix(Q, submxidx, 0)
		return sign

	# ----------------------------------------------------------------
	def householder_UT(self):
		[nr, nc] = self.dims()
		num_HH = nr
		if (nr > nc):
			num_HH = nc
		sign = 1
		for i in range(0, num_HH):
			sign *= self.householder_UT_pass_on_submatrix(i)
		return sign

	# ----------------------------------------------------------------
	# Decompose A into the product of orthogonal Q and upper-triangular R.
	# Do this using successive Householder transformations.

	# A:
	#   o o o o
	#   o o o o
	#   o o o o
	#   o o o o

	# Q1 A:
	#   o o o o
	#   . o o o
	#   . o o o
	#   . o o o

	# Q2 Q1 A:
	#   o o o o
	#   . o o o
	#   . . o o
	#   . . o o

	# Q3 Q2 Q1 A:
	#   o o o o
	#   . o o o
	#   . . o o
	#   . . . o

	# Now
	#   R = (Qn ... Q2 Q1) A.
	# Let
	#   Q = Qn ... Q2 Q1.
	# Then
	#   R = Q A.
	# Orthogonal matrices Q (e.g. Householders) have Q^t Q = I so we may
	# invert by transposing:
	#   A = Q^t R.

	# To do: doc pre-call alloc

	def QR_decomp(self, Q, R):
		tol = 1e-5 # To do: package the tol
		[nr, nc] = self.dims()
		num_HH = nr
		if (nr > nc):
			num_HH = nc

		# To do: check dims of Q and R
		# To do: also cmt why not alloc here (gc ...)
		Q.fill_identity_matrix()
		self.copy_elements_to(R)

		for i in range(0, num_HH):
			R.householder_UT_pass_on_submatrix(i, tol, Q)

		Q.transpose_in_place()

	# ----------------------------------------------------------------
	# http://en.wikipedia.org/wiki/Polar_decomposition.
	# A = U P
	# P = sqrt(A^* A)
	# U = A P^-1

	def polar_decomp(self):
		Astar = self.conjugate_transpose()
		ApA = Astar * self # To do: Perhaps make an A^* A method.
		P = ApA.sqrt()
		U = self * P.inv()
		return [U, P]

	# ----------------------------------------------------------------
	# To do: stub: not coded yet: could this sentence bear another colon: yes it
	# could: port me from HHUT.

	# o o o o o o
	# o o o o o o
	# . o o o o o
	# . o o o o o
	# . o o o o o
	# . o o o o o

	def upper_hessenberg_pass_on_submatrix(self, colidx, tol = 1e-5):
		[nr, nc] = self.dims()
		if (nr > nc):
			print >> sys.stderr, "upper_hessenberg_pass_on_submatrix:  I can't handle nr > nc."
			sys.exit(1)
		height = nr - colidx - 1
		if (colidx < 0 or colidx > nr or colidx > nc):
			print >> sys.stderr, \
				"upper_hessenberg_pass_on_submatrix:  column index %d out of bounds in %d x %d." \
				% (colidx, nr, nc)
			sys.exit(1)
		if (height < 1):
			return

		# Get the 1st column of the submatrix
		u = self.get_submatrix_column(colidx, colidx+1)

		# Compute ||u|| and v.
		v0 = math.sqrt(vecdot(u, u))
		if (u[0] >= 0):
			v0 = -v0
		v = [0] * height
		v[0] = v0

		# Compute axis = u - v.
		axis = vecsub(u, v)

		# Compute the Householder transformation.
		[Q, sign] = householder_vector_to_Q(axis)
		#Q.printp("Q")

		# Q: [1          ]  A: [o o o o o o]
		#    [  o o o o o]     [o o o o o o]
		#    [  o o o o o]     [. o o o o o]
		#    [  o o o o o]     [. o o o o o]
		#    [  o o o o o]     [. o o o o o]
		#    [  o o o o o]     [. o o o o o]

		# Q: [1          ]  A: [o o o o o o]
		#    [  1        ]     [o o o o o o]
		#    [    o o o o]     [. o o o o o]
		#    [    o o o o]     [. . o o o o]
		#    [    o o o o]     [. . o o o o]
		#    [    o o o o]     [. . o o o o]

		self.premultiply_by_submatrix(Q, colidx+1, colidx)
		self.postmultiply_by_submatrix_transpose(Q, colidx+1)

	# ----------------------------------------------------------------
	def to_upper_hessenberg_form(self, tol = 1e-5):
		[nr, nc] = self.dims()
		num_UH = nr
		if (nr > nc):
			num_UH = nc
		for i in range(0, num_UH):
			self.upper_hessenberg_pass_on_submatrix(i, tol)

	# ----------------------------------------------------------------
	def det(self):
		n = self.square_dim()

		if (n == 1):
			return self.elements[0][0]
		if (n == 2):
			a = self.elements[0][0]
			b = self.elements[0][1]
			c = self.elements[1][0]
			d = self.elements[1][1]
			return a*d - b*c

		# Make a copy
		A = sackmat(self.elements)

		# Use Householder transformations to put the matrix into
		# upper-triangular form.  Each transformation is (effectively) a
		# pre-multiplication by a Householder matrix with determinant -1.
		# Account for this below.
		sign = A.householder_UT()

		# Take the product along the diagonal.
		# The negative sign accounts for the factors of -1 introduced by
		# the Householder transformations.
		rv = sign
		for i in range(0, n):
			rv *= A[i][i]
		return rv

	# ----------------------------------------------------------------
	def trace(self):
		n = self.square_dim()
		rv = 0.0
		for i in range(0, n):
			rv += self.elements[i][i]
		return rv

	# ----------------------------------------------------------------
	# sum_i sum_k A_ik A_ki.
	def trace_of_square(self):
		n = self.square_dim()
		sum = 0.0
		for i in range(0, n):
			for k in range(0, n):
				sum += self.elements[i][k] * self.elements[k][i]
		return sum

	# ----------------------------------------------------------------
	# Does not check that the input is skew-symmetric.
	# Currently coded to use the recursive reduction formula:
	#   Pf(A) = sum_{k=1}^{N-1} (-1)^{k-1} A[0][k] Pf(Ahat[0][k])
	# where Ahat[j][k] excludes the jth and kth rows and columns from A.

	def pfaffian(self):
		N = self.square_dim()
		if (N & 1):
			print >> sys.stderr, "sackmat pfaffian: input dimension must be even; got %d." \
				% (N)
			sys.exit(1)
		if (N == 2):
			return (self.elements[0][1] - self.elements[1][0]) * 0.5

		sign = 1
		sum = 0.0
		for k in range(1, N):
			Ahat = self.pfaffian_hat(0, k)
			if (self.elements[0][k] != 0.0):
				# Avoid needless recurision if A[0][k] is zero.  This makes
				# significant performance improvement for large sparse matrices.
				sum = sum + sign * self.elements[0][k] * Ahat.pfaffian()
			sign = sign * -1
		return sum

	def pfaffian_hat(self, j, k):
		N = self.square_dim()
		rv = make_zero_matrix(N-2, N-2)
		di = 0
		for si in range(0, N):
			if (si != j and si != k):
				dj = 0
				for sj in range(0, N):
					if (sj != j and sj != k):
						rv[di][dj] = self[si][sj]
						dj += 1
				di += 1
		return rv

	# ----------------------------------------------------------------
	def augment_I(self):
		n = self.square_dim()
		AI = sackmat(self.elements)
		Z = [0] * n
		#print "1. AI\n", self
		for i in range (0, n):
			AI.elements[i] = AI.elements[i] + Z # Python list concatenation
		#print "2. AI\n", self
		for i in range (0, n):
			AI[i][n+i] = 1
		return AI

	# ----------------------------------------------------------------
	def inv(self, tol = 1e-6):
		n = self.square_dim()
		twon = n + n

		# First, paste the input and the identity side by side.
		AI = self.augment_I()

		# Second, use Householder transformations to put it into
		# upper-triangular form.
		AI.householder_UT()

		# Third, put 1 on the left diagonal.
		for i in range(0, n):
			d = AI[i][i]
			if (d == 0):
				print >> sys.stderr, "Singular."
				sys.exit(1)
			elif (abs(d) < tol):
				print >> sys.stderr, "Nearly singular."
				sys.exit(1)
			for j in range(0, twon):
				AI[i][j] = AI[i][j] / d

		# Fourth, clear out the rest of the left-hand side.
		# 1 . . . .  . . . . .
		# 0 1 . . .  . . . . .
		# 0 0 1 . .  . . . . .
		# 0 0 0 1 .  . . . . .  <-- i
		# 0 0 0 0 1  . . . . .  <-- i2

		i = n-2
		while (i >= 0):
			i2 = n-1
			while (i2 > i):
				mul = AI[i][i2]
				for j in range(0, twon):
					AI[i][j] -= AI[i2][j] * mul
				i2 -= 1
			i -= 1

		# Fifth, obtain the inverse from the right-hand side.
		for i in range(0, n):
			AI.elements[i] = AI.elements[i][n:twon]

		return AI

	# ----------------------------------------------------------------
	# This is a general row-reduction routine.  It operates on the matrix
	# in-place.  At the moment, it uses naive pivoting, appropriate for exact
	# arithmetic (e.g. finite fields).  For floating-point (here), it should be
	# re-coded to work harder to find the best row to pivot in.
	#
	# Also note that I prefer Householder-using algorithms when possible, which
	# in many cases avoid the need for row-reduction and pivoting in the first
	# place.  For more information please see http://johnkerl.org/doc/hh.pdf

	def row_reduce_below(self, tol=1e-7):
		[nr, nc] = self.dims()

		top_row = 0
		left_col = 0
		while (top_row < nr) and (left_col < nc):

			# Find the nearest row with a non-zero value in this column;
			# exchange that row with this one.
			pivot_row = top_row
			pivot_successful = 0
			while (not pivot_successful and (pivot_row < nr)):
				if (abs(self.elements[pivot_row][left_col]) >= tol):
					if (top_row != pivot_row):
						# Swap top row and pivot row
						temp = self.elements[top_row]
						self.elements[top_row] = self.elements[pivot_row]
						self.elements[pivot_row] = temp
					pivot_successful = 1
				else:
					pivot_row += 1
			if (not pivot_successful):
				left_col += 1
				continue # Work on the next column.

			# We can have a zero leading element in this row if it's
			# the last row and full of zeroes.
			top_row_lead = self.elements[top_row][left_col]
			if (abs(top_row_lead) >= tol):
				# Normalize this row.
				inv = 1.0 / top_row_lead
				for j in range(0, nc):
					self.elements[top_row][j] *= inv

				# Clear this column.
				top_row_lead = self.elements[top_row][left_col]
				for cur_row in range(top_row + 1, nr):
					current_row_lead = self.elements[cur_row][left_col]
					cr = self.elements[cur_row]
					tr = self.elements[top_row]
					for j in range(0, nc):
						self.elements[cur_row][j] = cr[j] * top_row_lead - tr[j] * current_row_lead
			left_col += 1
			top_row += 1
		return

	# ----------------------------------------------------------------
	# Operates on the matrix in-place.

	def row_echelon_form(self, tol=1e-7):
		[nr, nc] = self.dims()
		self.row_reduce_below(tol)

		for row in range(0, nr):
			for row2 in range(row+1, nr):
				[found, row2_leader_pos] = find_leader_pos(self.elements[row2], tol)
				if (not found):
					break

				row2_leader_val = self.elements[row2][row2_leader_pos]
				row_clear_val = self.elements[row][row2_leader_pos]
				if (abs(row_clear_val) < tol):
					continue

				mul = float(row_clear_val) / float(row2_leader_val)
				for j in range(0, nc):
					self.elements[row][j] -= self.elements[row2][j] * mul
		return

	# ----------------------------------------------------------------
	# This routine makes a copy of the matrix and row-reduces it.  To save
	# CPU cycles, use rank_rr() if the matrix is already row-reduced.

	def rank(self, tol=1e-7):
		Arr = sackmat(self.elements)
		Arr.row_reduce_below(tol)
		return Arr.rank_rr(tol)

	# ----------------------------------------------------------------
	# This routine assumes the matrix is already row-reduced.  If not,
	# use rank() instead.

	def rank_rr(self, tol=1e-7):
		[nr, nc] = self.dims()
		rank = 0

		for i in range(0, nr):
			row_is_zero = 1
			for j in range(0, nc):
				if (abs(self.elements[i][j]) >= tol):
					row_is_zero = 0
					break
			if (not row_is_zero):
				rank += 1
		return rank

	# ----------------------------------------------------------------
	def kernel_basis(self):
		[nr, nc] = self.dims()
		rr = sackmat(self.elements) # Make a copy
		rr.row_echelon_form()
		rank = rr.rank_rr()
		dimker = nc - rank

		if (dimker == 0):
			return [0, 0]

		kerbas = make_zero_matrix(dimker, nc)
		nfree = 0; # == dimker but I'll compute it anyway
		free_flags   = [1] * nc
		free_indices = [0] * nc

		for i in range(0, rank):
			[found, dep_pos] = find_leader_pos(rr[i])
			if (found):
				free_flags[dep_pos] = 0

		for i in range(0, nc):
			if (free_flags[i]):
				free_indices[nfree] = i
				nfree += 1

		# For each free coefficient:
		#   Let that free coefficient be 1 and the rest be zero.
		#   Also set any dependent coefficients which depend on that
		#   free coefficient.
		for i in range(0, dimker):
			kerbas[i][free_indices[i]] = 1

			# Matrix in row echelon form:
			#
			# 0210     c0 = ??      c0 = 1  c0 = 0
			# 1000     c1 = -2 c2   c1 = 0  c1 = 5
			# 0000     c2 = ??      c2 = 0  c2 = 1
			# 0000     c3 = 0       c3 = 0  c3 = 0

			# j  = 0,1
			# fi = 0,2

			# i = 0:
			#   j = 0  row 0 fi 0 = row 0 c0 = 0
			#   j = 1  row 1 fi 0 = row 1 c0 = 0
			# i = 1:
			#   j = 0  row 0 fi 1 = row 0 c2 = 2 dep_pos = 1
			#   j = 1  row 1 fi 1 = row 1 c2 = 0

			# 0001
			# 01?0

			for j in range(0, rank):
				if (tol_zero(rr[j][free_indices[i]])):
					continue

				[found, dep_pos] = find_leader_pos(rr[j])
				if (not found):
					print >> sys.stderr, "Coding error in get_kernel_basis!"
					sys.exit(1)

				kerbas[i][dep_pos] = -rr[j][free_indices[i]]

		# To do: temp jrk 2006-11-09
		# self.check_kernel_basis(kerbas, dimker)
		# To do: 2007-05-15:  The checker needs a fix but I don't remember the
		# data set which tripped it off.  I remember the problem was with
		# large numbers ... the check was using absolute instead of relative error.
		self.check_kernel_basis(kerbas, dimker)

		return [1, kerbas]

	# ----------------------------------------------------------------
	def check_kernel_basis(self, kerbas, dimker):
		for i in range(0, dimker):
			v = kerbas[i]
			Av = matrix_times_vector(self, v)
			if (not vector_is_zero(Av)):
				# To do: all this to stderr ...
				print >> sys.stderr, "Coding error in kernel basis."
				print "Coding error in kernel basis."; print
				self.printp("Matrix")
				print "dimker =", dimker
				kerbas.printp("Basis")
				print "Product at row " + str(i) + ":"
				print_row_vector(Av)
				sys.exit(1)

	# ----------------------------------------------------------------
	def get_column(self, j):
		[nr, nc] = self.dims()
		v = []
		for i in range(0, nr):
			v.append(self.elements[i][j])
		return v

	# ----------------------------------------------------------------
	def put_column(self, j, v):
		[nr, nc] = self.dims()
		for i in range(0, nr):
			self.elements[i][j] = v[i]

	# ----------------------------------------------------------------
	# Upper Hessenberg ...
	# generalize the HHUT method a bit ...

	# o o o o o o
	# . o o o o o
	# . . o o o o
	# . . . o o o
	# . . . . o o
	# . . . . . o

	# o o o o o o
	# o o o o o o
	# . o o o o o
	# . . o o o o
	# . . . o o o
	# . . . . o o

	# ----------------------------------------------------------------
	# Single QR decomposition ...

	# ----------------------------------------------------------------
	# Naive QR eigenvalue algorithm ...

	# ----------------------------------------------------------------
	# QR eigenvalue algorithm with upper Hessenberg ...

	# ----------------------------------------------------------------
	# At 171 iterations, 171! overflows a double-precision floating-point
	# number (~ 10^308).
	def exp(self, tol=1e-12, maxits=165):
		n = self.square_dim()
		k = 0
		B = make_zero_matrix(n, n)
		Ak = make_identity_matrix(n)
		kfact = 1

		while (1):
			#print "k =", k, "  k! =", kfact
			#print "A^%d =" % (k)
			#Ak.printf()
			#print

			worst = 0.0
			recip_kfact = 1.0 / kfact
			for i in range(0, n):
				for j in range(0, n):
					incrij = recip_kfact * Ak[i][j]
					B[i][j] += incrij

					absincrij = abs(incrij)
					if (absincrij > worst):
						worst = absincrij
			#print "worst=", worst

			if (worst < tol):
				break
			if (k > maxits):
				print >> sys.stderr, \
					"sackmat_m.exp:  max # iterations (%d) exceeded" \
					% (maxits)
				sys.exit(1)

			k += 1
			Ak *= self
			kfact *= k

		return B

	# ----------------------------------------------------------------
	# Denman-Beavers algorithm for matrix square root, for positive-definite A:
	# http://en.wikipedia.org/wiki/Matrix_square_root.
	#
	# Y_0 = A
	# Z_0 = I
	#
	# Y_{k+1} = 1/2 (Y_k + Z_k^-1)
	# Z_{k+1} = 1/2 (Z_k + Y_k^-1)
	#
	# Y_k converges quadratically to sqrt(A) and Z_k converges to sqrt(A)^-1.

	def sqrt(self):
		n  = self.square_dim()
		Yk = copy.copy(self)
		Zk = make_identity_matrix(n)

		k = 0
		maxiter = 100
		while (k < maxiter):

			Ykprev = Yk;           Zkprev = Zk
			Ykinv  = Yk.inv();     Zkinv  = Zk.inv()
			Yk     = Yk + Zkinv;   Zk     = Zk + Ykinv
			Yk.smul_in_place(0.5); Zk.smul_in_place(0.5)

			if (are_close_in_max_norm(Yk, Ykprev)):
				return Yk

			k += 1

		print >> sys.stderr, "sackmat.sqrt:  maxiter (%d) exceeded." \
			% (maxiter)
		sys.exit(1)

# ================================================================
def read_matrix(elt_scanner, file_name = "-"):
	A = []
	num_rows = 0

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	# Note that "for line in sys.stdin" slurps *all* the input.
	# We may not want all of it.
	while (1):
		line = file_handle.readline()
		if (line == ""):
			break

		# Strip comments.
		line = re.sub(r"#.*",  r"", line)
		# Strip leading and trailing whitespace.
		line = re.sub(r"^\s+", r"", line)
		line = re.sub(r"\s+$", r"", line)
		# Skip blank lines.
		if re.match(r"^$", line):
			continue

		v = row_vector_from_string(line, elt_scanner)
		if (v == []):
			if (num_rows > 0):
				break
		else:
			A.append(v)
			num_rows += 1

	if (file_name != "-"):
		file_handle.close()

	validate_matrix(A, "read_matrix")
	return sackmat(A)

# ----------------------------------------------------------------
def print_matrix(A, format="%11.7f"):
	A.printf(format)

def write_matrix(A, file_name, format="%11.7f"):
	[nr, nc] = A.dims()

	if (file_name == "-"):
		file_handle = sys.stdout
	else:
		try:
			file_handle = open(file_name, 'w')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for write."
			sys.exit(1)

	if isinstance(A.elements[0][0], complex):
		for i in range(0, nr):
			for j in range(0, nc):
				if (j > 0):
					file_handle.write(' ')
				rr = A.elements[i][j].real
				ii = A.elements[i][j].imag

				#file_handle.write(format % (rr))
				#file_handle.write(' ')
				#file_handle.write(format % (ii))

				# Use abs to handle the fact that IEEE floating-point has
				# signed zero.  I don't want to be printing "3+-0j" when
				# printing a conjugated real.
				file_handle.write(format % (rr))
				if (ii < 0):
					file_handle.write('-')
					file_handle.write(format % (abs(ii)))
				else:
					file_handle.write('+')
					file_handle.write(format % (abs(ii)))
				file_handle.write('j')
			file_handle.write('\n')
	else:
		for i in range(0, nr):
			for j in range(0, nc):
				if (j > 0):
					file_handle.write(' ')
				file_handle.write(format % (A.elements[i][j]))
			file_handle.write('\n')

	if (file_name != "-"):
		file_handle.close()

def write_matrix_as_column(A, file_name, format="%11.7f"):
	[nr, nc] = A.dims()

	if (file_name == "-"):
		file_handle = sys.stdout
	else:
		try:
			file_handle = open(file_name, 'w')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for write."
			sys.exit(1)

	if isinstance(A.elements[0][0], complex):
		for i in range(0, nr):
			for j in range(0, nc):
				if (j > 0):
					file_handle.write(' ')
				file_handle.write(format % (A.elements[i][j].real))
				file_handle.write(' ')
				file_handle.write(format % (A.elements[i][j].imag))
				file_handle.write('\n')
	else:
		for i in range(0, nr):
			for j in range(0, nc):
				if (j > 0):
					file_handle.write(' ')
				file_handle.write(format % (A.elements[i][j]))
				file_handle.write('\n')

	if (file_name != "-"):
		file_handle.close()

# ================================================================
# Binary I/O usage example:

# from sackmat_m import *
#
# A = sackmat([[1,2,3,4],[5,6,7,8]])
# A.printf()
# write_float_matrix_binary(A, 'd')
# print "\n"
#
# B = read_float_matrix_binary(2, 4, 'd')
# B.printf()
# print "\n"
#
# C = read_fcomplex_matrix_binary(2, 2, 'd')
# C.printf()
# print "\n"
#
# write_fcomplex_matrix_binary(C, 'e')

# ----------------------------------------------------------------
def read_float_matrix_binary(nr, nc, file_name):
	A = make_zero_matrix(nr, nc)
	fp = open(file_name, 'rb') # Use default exception handling
	bytes = fp.read(nr*nc*4)
	B = array.array('f',bytes)
	B.byteswap()
	k = 0
	for i in range(0, nr):
		for j in range(0, nc):
			A.elements[i][j] = B[k]
			k += 1
	fp.close()
	return A

# ----------------------------------------------------------------
def read_fcomplex_matrix_binary(nr, nc, file_name):
	A = make_zero_matrix(nr, nc)
	fp = open(file_name, 'rb') # Use default exception handling
	bytes = fp.read(nr*nc*8)
	B = array.array('f',bytes)
	B.byteswap()
	k = 0
	for i in range(0, nr):
		for j in range(0, nc):
			A.elements[i][j] = complex(B[k], B[k+1])
			k += 2
	fp.close()
	return A

def write_float_matrix_binary(A, file_name):
	[nr, nc] = A.dims()
	fp = open(file_name, 'wb') # Use default exception handling
	B = array.array('f')
	for i in range(0, nr):
		for j in range(0, nc):
			B.append(A.elements[i][j])
	B.byteswap()
	fp.write(B)
	fp.close()

# ----------------------------------------------------------------
def write_fcomplex_matrix_binary(A, file_name):
	[nr, nc] = A.dims()
	fp = open(file_name, 'wb') # Use default exception handling
	B = array.array('f')
	for i in range(0, nr):
		for j in range(0, nc):
			B.append(A.elements[i][j].real)
			B.append(A.elements[i][j].imag)
	B.byteswap()
	fp.write(B)
	fp.close()

# ================================================================
# Gram-Schmidt orthonormalization:
#
# Orthogonality step:
#   Input  {a_0 .. a_{n-1}}
#   Output {q_0 .. q_{n-1}}
#   q_0 = a_0
#   q_j = a_j - sum_{k=0}^{j-1} (a_j dot q_k)/(q_k dot q_k) q_k
# Normalization: q_j *= 1 / ||q_j||
#
# NOTE:  The matrix A is viewed as a container for row vectors.

def gram_schmidt(A, tol = 1e-7):
	[nr, nc] = A.dims()
	Q = sackmat(A.elements) # Make a copy

	# Orthogonality
	for j in range(0, nr):
		qj = Q[j]

		# q_j = a_j - sum_{k=0}^{j-1} (a_j dot q_k)/(q_k dot q_k) q_k

		for k in range(0, j):
			qk = Q[k]
			numer = vecdot(qj, qk)
			denom = vecdot(qk, qk)
			if (abs(denom) < tol):
				print >> sys.stderr, "Row ", k, " of Q is zero (or near-zero) in sackmat_m.gram_schmidt."
				sys.exit(1)
			quot = numer / denom
			qj = vecssub(qj, qk, quot)
		Q[j] = qj

	# Normalization
	for j in range(0, nr):
		qj = Q[j]
		dot = vecdot(qj, qj)
		if (dot < tol):
			print >> sys.stderr, "Row ", k, " of Q is zero (or near-zero) in sackmat_m.gram_schmidt."
			sys.exit(1)
		norm_recip = 1.0 / math.sqrt(dot)
		qj = vecsmul(qj, norm_recip)
		Q[j] = qj

	return Q

# ----------------------------------------------------------------
def kronecker_product(A, B):
	[anr, anc] = A.dims()
	[bnr, bnc] = B.dims()
	cnr = anr*bnr
	cnc = anc*bnc
	C = make_zero_matrix(cnr, cnc)
	for ai in range(0, anr):
		for bi in range(0, bnr):
			ci = ai*bnr + bi
			for aj in range(0, anc):
				for bj in range(0, bnc):
					cj = aj*bnc + bj
					C.elements[ci][cj] = A.elements[ai][aj] * B.elements[bi][bj]
	return C

# ----------------------------------------------------------------
# E.g. multikron([A, B, C]) is the Kronecker product of the matrices A, B, and
# C.  The Kronecker product is associative so this is well-defined.
def multikron(mxlist):
	if (mxlist == []):
		return []
	rv = mxlist[0]
	for i in range(1, len(mxlist)):
		rv = kronecker_product(rv, mxlist[i])
	return rv

# ----------------------------------------------------------------
# The k-fold Kronecker product of the specified matrix A at the i'th slot
# and the identity matrix at all other slots.
#
# Example:
#   multikroni(A, 2, 4)
# gives the same result as
#   multikron([I, I, A, I]).
def multikroni(A, i, k):
	n = A.square_dim()
	I = make_identity_matrix(n)
	list = []
	for j in range(0, k):
		if (i == j):
			list.append(A)
		else:
			list.append(I)
	return multikron(list)

# ----------------------------------------------------------------
def vkron(u, v):
	m = len(u)
	n = len(v)
	mn = m*n
	w = [0.0] * mn
	k = 0
	for i in range(0, m):
		for j in range(0, n):
			w[k] = u[i] * v[j]
			k += 1
	return w

# ----------------------------------------------------------------
# E.g. multivkron([u, v, w]) is the Kronecker product of the vectors u, v, and
# w.  The Kronecker product is associative so this is well-defined.
def multivkron(veclist):
	if (veclist == []):
		return []
	rv = veclist[0]
	for i in range(1, len(veclist)):
		rv = vkron(rv, veclist[i])
	return rv

### ----------------------------------------------------------------
##def matuneg
##	(aref, nr, nc) = _
##
##	die "matuneg():  Need as arguments matrix reference and dimensions.\n"
##		unless defined nc
##
##	for (i = 0; i < nr; i++):
##		for (j = 0; j < nc; j++):
##			N[i][j] = -aref[i][j]
##	return N

### ----------------------------------------------------------------
##def matuneg_in_place
##	(aref, nr, nc) = _
##
##	die
##	"matuneg_in_place():  Need as arguments matrix reference and dimensions.\n"
##		unless defined nc
##
##	for (i = 0; i < nr; i++):
##		for (j = 0; j < nc; j++):
##			aref[i][j] = -aref[i][j]

# ----------------------------------------------------------------
# Jacobi real-symmetric eigensolver.  At present, this is coded very naively.
# Loosely adapted from Numerical Recipes.

def rs_eigensystem(self):
	# Make a copy
	A = sackmat(self.elements)
	n = A.square_dim()
	V = make_identity_matrix(n)
	maxiter = 20

	iter = 0
	while (1):
		iter += 1

		sum = 0.0
		for i in range(1, n):
			for j in range(0, i):
				sum += abs(A.elements[i][j])
		#print "sum at iteration %d is %11.7e" % (iter, sum); print
		if (tol_zero(sum**2, 1e-12)):
			break

		if (iter > maxiter):
			print >> sys.stderr, \
				"Jacobi eigensolver: max iterations (%d) exceeded.  Non-symmetric input?" \
				% (maxiter)
			sys.exit(1)

		for p in range(0, n):
			for q in range(p+1, n):
				numer = A.elements[p][p] - A.elements[q][q]
				denom = A.elements[p][q] + A.elements[q][p]
				if (tol_zero(denom)):
					continue
				theta = (1.0*numer) / denom
				sign_theta = 1
				if (theta < 0):
					sign_theta = -1
				t = sign_theta / (abs(theta) + math.sqrt(theta**2 + 1))
				c = 1.0 / math.sqrt(t**2 + 1)
				s = t * c

				# This is wasteful memory allocation.
				P = make_identity_matrix(n)
				P[p][p] =  c
				P[p][q] = -s
				P[q][p] =  s
				P[q][q] =  c

				PT = P.transpose()
				A = PT * A * P
				V = V * P

				#print "theta=%11.7f sign_theta=%11.7f" % (theta, sign_theta)
				#print "c=%11.7f s=%11.7f" % (c, s)
				#print "P^t[%d][%d]:" % (p,q); PT.printf(); print ""
				#print "P[%d][%d]:"   % (p,q); P.printf();  print ""
				#print "A[%d][%d]:"   % (p,q); A.printf();  print ""
				#print "V[%d][%d]:"   % (p,q); V.printf();  print ""

	return [V, A]

### ----------------------------------------------------------------
##def matsmul
##	my (aref, anr, anc, scalar, cref) = _
##	my (i, j)
##
##	die "matsmul():  Need as arguments two matrix references and dimensions.\n"
##		unless defined cref
##	for (i = 0; i < anr; i++):
##		for (j = 0; j < anc; j++):
##			cref[i][j] = scalar * aref[i][j]

# ----------------------------------------------------------------
# To do: tol_zero, tol_non_zero routines.  Fold into sackutil. Also have
# the latter export the tol.

# ----------------------------------------------------------------
# Plan:
# * QR decomp (done) -> SVD?  Or SVD via Jacobi?  U:AAt/V:AtA?  Check it out.
#   - Do AtA and AAt share common eigenvalues?  Does eig(AB) == eig(BA)?
#   - Singular values of A are the square roots of the eigenvalues of AtA.
#     This is the definition of singular value.
# * Asymmetrical eigensolver:  general matrix -> UH via HH's.  Then QR decomp.
# * Complexify all, after real implementation.

# ----------------------------------------------------------------
# Jacobi:
# * Re-do it legibly (non-NR).

# ----------------------------------------------------------------
# UH:

# ----------------------------------------------------------------
# QR:
# * A = input
# * A1 = A
# * A1 = Q1 R1
# * A2 = R1 Q1
#   Note
#   A2 = R1 Q1
#      = Q1t Q1 R1 Q1
#      = Q1t A1 Q1
#   -- similar, so same eivals.
# * Oscillation in the presence of non-real eigenvalues?
