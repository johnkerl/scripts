#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2005-11-07
#
# This is a Python library for simple I/O and arithmetic on vectors
# and matrices of floating-point numbers.
# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# ================================================================

# xxx tol_zero, tol_non_zero routines.  fold into sackutil. *also* have
# the latter export the tol

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import copy
import re
import math
import array # For binary I/O
import types

# ----------------------------------------------------------------
def check_same_matrix_dims(A, B, func_name):
	# xxx check is-list twice
	[anr, anc] = A.dims()
	[bnr, bnc] = B.dims()
	if (anr != bnr) or (anc != bnc):
		print "%s: mismatched lengths %dx%d, %dx%d." % (func_name, anr, anc, bnr, bnc)
		sys.exit(1)
	return [anr, anc]

# ----------------------------------------------------------------
def check_mul_matrix_dims(A, B, func_name):
	# xxx check is-list x 4
	[anr, anc] = A.dims()
	[bnr, bnc] = B.dims()
	if (anc != bnr):
		print "%s: mismatched mul lengths %dx%d, %dx%d." % (func_name, anr, anc, bnr, bnc)
		sys.exit(1)
	return [anr, anc, bnr, bnc]


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
def matrix_times_vector(A, v):
	Av = []
	[nr, nc] = A.dims()
	n = len(v)
	for i in range(0, nr):
		Av.append(vecdot(A[i], v))
	return Av

# ----------------------------------------------------------------
def vecadd(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecadd")
	n = len(u)
	w = []
	for i in range(0, n):
		w.append(u[i] + v[i])
	return w

# ----------------------------------------------------------------
def vecsub(u, v):
	#n = check_same_list_dims(u, v, "sackmat vecsub")
	n = len(u)
	w = []
	for i in range(0, n):
		w.append(u[i] - v[i])
	return w

# ----------------------------------------------------------------
def vecsub_with_smul(u, v, s):
	#n = check_same_list_dims(u, v, "sackmat vecsub")
	n = len(u)
	w = []
	for i in range(0, n ):
		w.append(u[i] - s*v[i])
	return w;

# ----------------------------------------------------------------
def vecdot(u, v):
	s = 0
	n = len(u)
	#n = check_same_list_dims(u, v, "sackmat vecdot")
	for i in range(0, n):
		s += u[i] * v[i]
	return s

# ----------------------------------------------------------------
def vecnorm(u):
	return math.sqrt(vecdot(u, u))

# ----------------------------------------------------------------
def vecsmul(u, s):
	v = []
	for ue in u:
		v.append(ue * s)
	return v

# ----------------------------------------------------------------
def print_row_vector(v, format="%7.4f"):
	n = len(v)
	for i in range(0, n):
		print v[i],
	print

# ----------------------------------------------------------------
def print_column_vector(v, format="%7.4f"):
	n = len(v)
	for i in range(0, n):
		print v[i]

# ----------------------------------------------------------------
def row_vector_from_string(orig_line, elt_scanner):
	v = []
	line = copy.copy(orig_line)

	# Chomp trailing newline, if any.
	if (line[-1] == '\n'):
		line = line[0:-1]

	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	if (line == ""):
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

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	# Note that "for line in sys.stdin" slurps *all* the input.
	# We may not want all of it.
	line = ""
	while (line == ""):
		line = file_handle.readline()

	v = row_vector_from_string(line, elt_scanner)
	if (v == []):
		print "sackmat read_row_vector: empty input."
		sys.exit(1)

	if (file_name != "-"):
		file_handle.close()

	return v

# ----------------------------------------------------------------
def read_column_vector(elt_scanner, file_name = "-"):
	v = []

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	# Note that "for line in sys.stdin" slurps *all* the input.
	# We may not want all of it.
	while (1):
		line = file_handle.readline()
		if (line == ""):
			break
		elt = elt_scanner(line)
		v.append(elt)

	if (file_name != "-"):
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
		if (abs(v[j]) >= tol):
			return [1, j]
	return [0, 0]

def tol_zero(x, tol=1e-7):
	if (abs(x) < tol):
		return 1
	else:
		return 0

# ----------------------------------------------------------------
def vector_is_zero(v, tol=1e-7):
	n = len(v)
	for i in range(0, n):
		if (not tol_zero(v[i])):
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
	aa = vecdot(a, a) # xxx needs divide-by-zero check
	# The cast to float is in case the inputs are integers.
	u_par = vecsmul(a, float(ua)/float(aa))
	return u_par

def projperp(u, a):
	u_par = projpar(u, a)
	u_perp = vecsub(u, u_par)
	return u_perp


# ----------------------------------------------------------------
# Q = I - 2 v v^t / (v^t v)

def householder_v_to_Q(v):
	# xxx package the tol ...
	tol = 1e-10
	n = len(v)
	v_dot_v = vecdot(v, v)
	Q = make_identity_matrix(n)
	if (v_dot_v >= tol):
		two_over_v_dot_v = 2.0 / v_dot_v
		for i in range(0, n):
			for j in range(0, n):
				Q[i][j] -= v[i]*v[j] * two_over_v_dot_v
	return Q

# ----------------------------------------------------------------
def validate_matrix(A, func_name):
	#xxx is-list A -- put into sackutil
	nr = len(A)
	if (nr < 1):
		print func_name + ":  no rows."
		sys.exit(1)
	nc = len(A[0])
	if (nc < 1):
		print func_name + ":  empty row."
		sys.exit(1)
	for row in A:
		if (len(row) != nc):
			print func_name + ":  ragged input."
			sys.exit(1)
	return [nr, nc]

# ================================================================
class sackmat:

	def __init__(self, elements):
		# xxx validate
		self.elements = copy.deepcopy(elements)

	def dims(self):
		return [len(self.elements), len(self.elements[0])]

	def square_dim(self):
		[nr, nc] = self.dims()
		if (nr != nc):
			print "Non-square input."
			sys.exit(1)
		return nr

	def num_rows(self):
		return len(self.elements)
	def num_cols(self):
		return len(self.elements[0])

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

	def __mul__(A, B):
		[anr, anc, bnr, bnc] = check_mul_matrix_dims(A, B, "sackmat mul")
		C = make_zero_matrix(anr, bnc)
		for i in range(0, anr):
			for j in range(0, bnc):
				C[i][j] = 0
				for k in range(0, anc):
					C[i][j] += A[i][k] * B[k][j]
		return C

	def __neg__(A):
		[nr, nc] = A.dims()
		C = make_zero_matrix(nr, nc)
		for i in range(0, nr):
			for j in range(0, nc):
				C[i][j] = -A[i][j]
		return C

	def smul(self, s):
		[nr, nc] = self.dims()
		C = make_zero_matrix(nr, nc)
		for i in range(0, nr):
			for j in range(0, nc):
				C[i][j] = s * self.elements[i][j]
		return C

	def to_scalar(self):
		[nr, nc] = self.dims()
		if (nr != 1 or nc != 1):
			print "sackmat to_scalar: input dimensions must be 1x1; got %dx%d." \
				% (nr, nc)
			sys.exit(1)
		# Also try to hande the case when it's bigger than 1x1, but
		# is a scalar multiple of the identity (to within a tolerance).
		return self.elements[0][0]

	def transpose(self):
		nr = len(self.elements)
		nc = len(self.elements[0])
		C = make_zero_matrix(nc, nr)
		for i in range(0, nr):
			for j in range(0, nc):
				C[j][i] = self.elements[i][j]
		return C

	def __str__(self):
		nr = len(self.elements)
		nc = len(self.elements[0])
		mat_string = ""
		for i in range(0, nr):
			row_string = str(self.elements[i][0])
			for j in range(1, nc):
				row_string += " " + str(self.elements[i][j])
			mat_string += row_string + "\n"
		return mat_string

	def printf(self, format="%7.4f"):
		nr = len(self.elements)
		nc = len(self.elements[0])
		if isinstance(self.elements[0][0], complex):
			for i in range(0, nr):
				for j in range(0, nc):
					print format % (self.elements[i][j].real),
					print format % (self.elements[i][j].imag),
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
		return submatrix_column;

	def put_submatrix_column(self, colidx, start_row, column):
		[nr, nc] = self.dims()
		src = 0
		for dst in range(start_row, nr):
			self.elements[dst][colidx] = column[src];
			src += 1
		return

	# ----------------------------------------------------------------
	# all I need is HH on submx ...
	# implement more?

	# [ * * * * * ]
	# [ * * * * * ]
	# [ * * * * * ]
	# [ * * * * * ]

	# [ * * * * * ]
	# [ 0 * * * * ]
	# [ 0 * * * * ]
	# [ 0 * * * * ]

# * get submx
# * put submx
# * get column
# * v to w and z
# * z to Q

	# ----------------------------------------------------------------
	def householder_on_submatrix(self, a, tol = 1e-5):
		# Just extract and replace the submx.
		[nr, nc] = self.dims()
		height = nr - a

		# --- First column ---
		# Get v
		v = self.get_submatrix_column(a, a)

		# Compute ||v|| write w.
		normv = math.sqrt(vecdot(v, v))
		if (v[0] >= 0):
			normv = -normv

		w = [0] * height
		w[0] = normv

		# Compute z = v - w.
		z = vecsub(v, w)

		self.put_submatrix_column(a, a, w)

		# Compute 2 * (z dot z)
		zdotz = vecdot(z, z)
		if (abs(zdotz) < tol):
			tnz2 = 0
		else:
			tnz2 = 2.0 / zdotz

		# --- Subsequent columns ---
		for b in range (a+1, nc):
			c = self.get_submatrix_column(b, a)

			# Compute the scalar z^t c
			ztc = vecdot(z, c)

			# Compute d = (-2 / z dot z) * z^t c
			d = -tnz2 * ztc

			# New column is q = c + d * z.
			for j in range(0, height):
				w[j] = c[j] + d * z[j]

			self.put_submatrix_column(b, a, w)

		return

	# ----------------------------------------------------------------
	def det(self):
		n = self.square_dim()
		# Make a copy
		A = sackmat(self.elements)

		# Use Householder transformations to put the matrix into
		# upper-triangular form.  Each transformation is (effectively) a
		# pre-multiplication by a Householder matrix with determinant -1.
		# Account for this below.
		for i in range(0, n):
			A.householder_on_submatrix(i)

		# Take the product along the diagonal.
		# The negative sign accounts for the factors of -1 introduced by
		# the Householder transformations.
		rv = 1.0
		for i in range(0, n):
			rv *= -A[i][i]
		return rv

	# ----------------------------------------------------------------
	# Does not check that the input is skew-symmetric.
	# Currently coded to use the recursive reduction formula:
	#   Pf(A) = sum_{k=1}^{N-1} (-1)^{k-1} A[0][k] Pf(Ahat[0][k])
	# where Ahat[j][k] excludes the jth and kth rows and columns from A.

	def pfaffian(self):
		N = self.square_dim()
		if (N & 1):
			print "sackmat pfaffian: input dimension must be even; got %d." \
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
		for i in range(0, n):
			AI.householder_on_submatrix(i)

		# Third, put 1 on the left diagonal.
		for i in range(0, n):
			d = AI[i][i]
			if (d == 0):
				print "Singular."
				sys.exit(1)
			elif (abs(d) < tol):
				print "Nearly singular."
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
	# in-place.  At the moment, it uses is naive pivoting, appropriate for
	# exact arithmetic (e.g. finite fields).  For floating-point (here), it
	# should be re-coded to work harder to find the best row to pivot in.

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
					print "Coding error in get_kernel_basis!"
					sys.exit(1)

				kerbas[i][dep_pos] = -rr[j][free_indices[i]]

		# xxx temp jrk 2006-11-09
		# self.check_kernel_basis(kerbas, dimker)

		return [1, kerbas]

	# ----------------------------------------------------------------
	def check_kernel_basis(self, kerbas, dimker):
		for i in range(0, dimker):
			v = kerbas[i]
			Av = matrix_times_vector(self, v)
			if (not vector_is_zero(Av)):
				print "Coding error in kernel basis."; print
				print "Matrix:"; self.printf(); print
				print "dimker =", dimker
				print "Basis:"; kerbas.printf(); print
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
			print "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	# Note that "for line in sys.stdin" slurps *all* the input.
	# We may not want all of it.
	while (1):
		line = file_handle.readline()
		if (line == ""):
			break
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
def write_matrix(A, format="%7.4f"):
	A.printf(format)

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
				print "Row ", k, " of Q is zero (or near-zero) in sackmat_m.gram_schmidt."
				sys.exit(1)
			quot = numer / denom
			qj = vecsub_with_smul(qj, qk, quot)
		Q[j] = qj

	# Normalization
	for j in range(0, nr):
		qj = Q[j]
		dot = vecdot(qj, qj)
		if (dot < tol):
			print "Row ", k, " of Q is zero (or near-zero) in sackmat_m.gram_schmidt."
			sys.exit(1)
		norm_recip = 1.0 / math.sqrt(dot)
		qj = vecsmul(qj, norm_recip)
		Q[j] = qj

	return Q

# ----------------------------------------------------------------
def kernel_basis(self):
#	[nr, nc] = self.dims()
#	rr = sackmat_m(self.elements) # Make a copy
#	rr.row_echelon_form()
#	rank = rr.rank_rr()
#	dimker = nc - rank
#
##	return 0 if (dimker == 0)
##
##	kerbas = make_zero_matrix(dimker, nc)
##
##	nfree = 0; # == dimker but I'll compute it anyway
##
#	free_flags = [0] * nc
##
##	for (i = 0; i < rank; i++):
##		rowcopy = get_row(rr, nr, nc, i)
##		if (find_leader_pos(rowcopy, nc, \dep_pos)):
##			free_flags[dep_pos] = 0
##
##	for (i = 0; i < nc; i++):
##		if (free_flags[i]):
##			free_indices[nfree++] = i
##
##	# For each free coefficient:
##	#   Let that free coefficient be 1 and the rest be zero.
##	#   Also set any dependent coefficients which depend on that
##	#   free coefficient.
##	for (i = 0; i < dimker; i++):
##		kerbas[i][free_indices[i]] = 1.0
##
##		# Matrix in row echelon form:
##		#
##		# 0210     c0 = ??      c0 = 1  c0 = 0
##		# 1000     c1 = -2 c2   c1 = 0  c1 = 5
##		# 0000     c2 = ??      c2 = 0  c2 = 1
##		# 0000     c3 = 0       c3 = 0  c3 = 0
##
##		# j  = 0,1
##		# fi = 0,2
##
##		# i = 0:
##		#   j = 0  row 0 fi 0 = row 0 c0 = 0
##		#   j = 1  row 1 fi 0 = row 1 c0 = 0
##		# i = 1:
##		#   j = 0  row 0 fi 1 = row 0 c2 = 2 dep_pos = 1
##		#   j = 1  row 1 fi 1 = row 1 c2 = 0
##
##		# 0001
##		# 01?0
##
##		for (j = 0; j < rank; j++):
##			next if (tol_zero(rr[j][free_indices[i]]))
##
##			rowcopy = get_row(rr, nr, nc, j)
##			if (!find_leader_pos(rowcopy, nc, \dep_pos)):
##				die "Coding error in get_kernel_basis!\n"
##
##			kerbas[i][dep_pos] = -rr[j][free_indices[i]]
##
##	# #ifdef KERBAS_DEBUG
##	#	std::cout << "start check:\n"
##	#	std::cout << "A  =\n" << *this << "\n"
##	#	std::cout << "rr =\n" << rr << "\n"
##	#
##	#	for (i = 0; i < dimker; i++):
##	#		std::cout << "v  = " << kerbas.rows[i] << "\n"
##	#	std::cout << "\n"
##	#	for (i = 0; i < dimker; i++):
##	#		tvector Av = *this * kerbas.rows[i]
##	#		std::cout << "Av = " << Av << "\n"
##	#	std::cout << "end check.\n"
##	#	std::cout << "\n"
##	# #endif # KERBAS_DEBUG
##
##	check_kernel_basis(aref, nr, nc, kerbas, dimker)
##
##	basisref = kerbas
##	dimref = dimker
##
	return 1

### ----------------------------------------------------------------
##def check_kernel_basis
##	(aref, nr, nc, basisref, dimker) = _
##	for (i = 0; i < dimker; i++):
##		v = get_row(basisref, dimker, nc, i)
##		Av = matrix_times_vector(aref, nr, nc, v, nc)
##		if (!vector_is_zero(Av, nr)):
##			print "Coding error in kernel basis.\n"
##			print "Matrix:\n"
##			print_matrix(aref, nr, nc)
##			print "Basis:\n"
##			print_matrix(basisref, dimker, nc)
##			print "Product at row i:\n"
##			print_row_vector(Av, nr)
##			die

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

### ----------------------------------------------------------------
### At present, this is coded very naively.  Loosely adapted from Numerical Recipes.
##
##def rs_eigensystem(self):
##	my (aref, n, dref, vref) = _
##	my (p, q)
##	my A = copy_matrix(aref, n, n)
##	my V = make_I(n)
##	my maxiter = 20
##
##	for (s = 0; ; s++):
##		my sum = 0
##		for (i = 1; i < n; i++):
##			for (j = 0; j < i; j++):
##				sum += abs(A[i][j])
##		#printf "sum at iteration s is %11.7e\n", sum
##		last if (tol_zero(sum**2))
##
##		if (s > maxiter):
##			die "Jacobi eigensolver: max iterations (maxiter) exceeded.  Non-symmetric input?\n"
##
##		for (p = 0; p < n; p++):
##			for (q = p+1; q < n; q++):
##
##				my numer = A[p][p] - A[q][q]
##				my denom = A[p][q] + A[q][p]
##				next if (tol_zero(denom))
##				my theta = numer / denom
##				my sign_theta = (theta < 0) ? -1 : 1
##				my t = sign_theta / (abs(theta) + math.sqrt(theta**2 + 1))
##				my c = 1.0 / math.sqrt(t**2 + 1)
##				my s = t * c
##				my P = make_I(n)
##				P[p][p] =  c
##				P[p][q] = -s
##				P[q][p] =  s
##				P[q][q] =  c
##
##				#print "\n"
##				#print "P[p][q]:\n"
##				#print_matrix(P, n, n)
##
##				my foo = n
##				my bar = n
##
##				my PT = P
##				transpose_in_place(PT, \foo, \bar)
##
##				#print "\n"
##				#print "PT[p][q]:\n"
##				#print_matrix(PT, n, n)
##
##				matmul(PT, n, n, A, n, n, A, \foo, \bar)
##				matmul(A,  n, n, P, n, n, A, \foo, \bar)
##				matmul(V,  n, n, P, n, n, V, \foo, \bar)
##
##				#print "\n"
##				#print "A:\n"
##				#print_matrix(A, n, n)
##
##				#print "\n"
##				#print "V:\n"
##				#print_matrix(V, n, n)
##
##	dref = copy_matrix(A, n, n)
##	vref = copy_matrix(V, n, n)

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

### ----------------------------------------------------------------
##def get_row
##	my (aref, nr, nc, rowidx) = _
##	my j
##	my row
##	for (j = 0; j < nc; j++):
##		row[j] = aref[rowidx][j]
##	return row

### ----------------------------------------------------------------
##def put_row
##	my (aref, nr, nc, rowidx, prowref) = _
##	my j
##	for (j = 0; j < nc; j++):
##		aref[rowidx][j] = prowref[j]

