#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from sackmat_m import *

# ----------------------------------------------------------------
def rrb_test():
	#A = sackmat([[1,2,3],[4,5,6],[7,8,9]])
	A = sackmat([[0,0,0],[0,1,0],[0,0,1]])
	print "A:"
	A.printf()
	A.row_reduce_below()
	print "rrb A:"
	A.printf()

# ----------------------------------------------------------------
def re_test():
	A = sackmat([[1,2,3],[4,5,6],[7,8,9]])
	#A = sackmat([[0,0,0],[0,1,0],[0,0,1]])
	print "A:"
	A.printf()
	A.row_echelon_form()
	print "rech A:"
	A.printf()

# ----------------------------------------------------------------
def gs_test():
	#A = sackmat([[1,0,0],[0,1,0],[0,1,1]])
	#A = sackmat([[2,0,0],[2,2,0],[2,2,2]])
	A = sackmat([[0,0,1],[0,2,2],[3,3,3]])
	print "A:"
	A.printf()
	B = gram_schmidt(A)
	print "GS A:"
	B.printf()

# ----------------------------------------------------------------
def sack_mat_test():
	A = sackmat([[1,2,3],[4,5,6]]); print "A:\n", A
	B = sackmat([[1,2,3],[4,5,6]]); print "B:\n", B
	C = A + B; print "C:\n", C
	C = A - B; print "C:\n", C
	B = sackmat([[1,2],[3,4],[5,6]]); print "B:\n", B
	C = A * B; print "C:\n", C

	At = A.transpose();
	print "A:\n", A
	print "A^t:\n", At

	A = sackmat([[1,2,3],[4,5,6],[7,8,9]])
	At = A.transpose();
	print "A:\n", A
	SA = A + At;
	print "Sym(A):\n", SA
	AA = A - At;
	print "Sym(A):\n", AA
	print

	print "A:\n", A
	A.householder_on_submatrix(1)
	print "hh 1 A:\n", A

	A = sackmat([[1,2,3],[4,5,6],[7,8,9]])
	print "A:\n", A
	d = A.det()
	print "det(A):", d

	A = make_identity_matrix(4)
	print "A:\n", A
	d = A.det()
	print "det(A):", d

	A = read_matrix(float,'a')
	print "A from file:\n", A

	A = make_identity_matrix(4)
	print "A:\n", A
	B = A.inv()
	print "inv(A):\n", B
	C = A * B
	print "A * inv(A):\n", C

	A = sackmat([[0,1,0],[0,0,1],[1,1,0]])
	print "A:\n", A
	B = A.inv()
	print "inv(A):\n", B
	C = A * B
	print "A * inv(A):\n", C

	A = sackmat([[-1,2,3],[4,-5,6],[7,8,-9]])
	print "A:\n", A
	B = A.inv()
	print "inv(A):\n", B
	C = A * B
	print "A * inv(A):\n", C

# ----------------------------------------------------------------
def proj_perp_test():
	#u = [4,3]
	#a = [1,1]

	u = [4,3]
	a = [1,1]

	u_par  = projpar(u, a)
	u_perp = projperp(u, a)

	nu = vecnorm(u)
	npar = vecnorm(u_par)
	nperp = vecnorm(u_perp)
	print "u=    ", u
	print "a=    ", a
	print "par=  ", u_par
	print "perp= ", u_perp
	print nu, npar, nperp, math.sqrt(npar**2 + nperp**2)

# ----------------------------------------------------------------
def kerbas_test():
	#A = sackmat([[1,2,3],[4,5,6]])
	A = sackmat([[1,2,3],[3,7,4]])
	print "A:"
	A.printf()
	print
	[found, B] = A.kernel_basis()
	print "A:"
	A.printf()
	if (found):
		print
		print "kerbas:"
		B.printf()
	else:
		print "Empty basis"

# ----------------------------------------------------------------
#rrb_test()
#re_test()
#gs_test()
#sack_mat_test()
#proj_perp_test()
kerbas_test()
