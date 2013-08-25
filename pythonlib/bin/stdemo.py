#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from sackmat_m import *
from sackst_m import *
import random

# ----------------------------------------------------------------
def maindemo():
	n = 3
	for r in range(0, 5):
		A = make_zero_simple_tensor(r, n); print r, n; A.printf()

	n = 4
	for r in range(0, 5):
		A = make_I_simple_tensor(r, n); print r, n; A.printf()

	n = 4
	for r in range(0, 5):
		A = make_ones_simple_tensor(r, n); print r, n; A.printf()

	n = 2
	A = make_zero_simple_tensor(3, n);
	B = make_zero_simple_tensor(3, n);
	for i in range(0, n):
		for j in range(0, n):
			for k in range(0, n):
				A[i][j][k] = i+j+k + i*j*k + 1
				B[i][j][k] = 2+i
	C = A + B
	print "A:"; A.printf()
	print "B:"; B.printf()
	print "A+B:"; C.printf()

	A = simple_tensor([[1,2],[3,4]])
	B = simple_tensor([5, 6])
	C = A * B
	print "A:"; A.printf()
	print "B:"; B.printf()
	print "A*B:"; C.printf()

	A = simple_tensor([[1,2],[3,4]])
	B = simple_tensor([5, 6])
	C = B * A
	print "A:"; A.printf()
	print "B:"; B.printf()
	print "B*A:"; C.printf()

	A = simple_tensor([[1,2,3],[4,5,6],[7,8,9]])
	B = simple_tensor([-1, -2, -3])
	C = A * B
	print "A:"; A.printf()
	print "B:"; B.printf()
	print "A*B:"; C.printf()

	A = simple_tensor(2)
	B = simple_tensor(3)
	print "A:"; A.printf()
	print "B:"; B.printf()
	C = A * B
	print "A*B:"; C.printf()

	A = simple_tensor([[1,2,3],[4,5,6],[7,8,9]])
	print "A:"; A.printf()
	B = A.Alt()
	print "Alt(A):"; B.printf()
	B = A.Sym()
	print "Sym(A):"; B.printf()

	A = simple_tensor([[[1,4],[3,2]],[[9,6],[7,5]]])
	print "A:"; A.printf()
	B = A.Alt()
	print "Alt(A):"; B.printf()
	B = A.Sym()
	print "Sym(A):"; B.printf()
	print

	X = simple_tensor([[1,2,3],[4,5,6],[7,8,9]])
	Y = simple_tensor([1,-1,1])
	P = X * Y
	S = X & Y
	A = X ^ Y
	print "X:";   X.printf()
	print "Y:";   Y.printf()
	print "X*Y:"; P.printf()
	print "XY:";  S.printf()
	print "X^Y:"; A.printf()
	print

	X = simple_tensor([[1,2,3],[4,5,6],[7,8,9]])
	Y = simple_tensor([[1,2,3],[4,5,6],[7,8,9]])
	P = X * Y
	S = X & Y
	A = X ^ Y
	print "X:";   X.printf()
	print "Y:";   Y.printf()
	print "X*Y:"; P.printf()
	print "XY:";  S.printf()
	print "X^Y:"; A.printf()
	print

	X = simple_tensor([[1,0,0],[0,1,0],[0,0,1]])
	Y = simple_tensor([1,1,1])
	P = X * Y
	S = X & Y
	A = X ^ Y
	print "X:";   X.printf()
	print "Y:";   Y.printf()
	print "X*Y:"; P.printf()
	print "XY:";  S.printf()
	print "X^Y:"; A.printf()
	print

	X = make_I_simple_tensor(2, 4)
	Y = make_I_simple_tensor(2, 4)
	P = X * Y
	S = X & Y
	A = X ^ Y
	print "X:";   X.printf()
	print "Y:";   Y.printf()
	print "X*Y:"; P.printf()
	print "XY:";  S.printf()
	print "X^Y:"; A.printf()
	print

	n = 3
	for i in range(0, n):
		ei = simple_tensor(sackmat_m.stdbv(i, n))
		for j in range(i+1, n):
			ej = simple_tensor(sackmat_m.stdbv(j, n))
			eij = ei ^ ej
			print "e" + str(i) + " ^ e" + str(j)
			eij.printf()

	n = 3
	for i in range(0, n):
		ei = simple_tensor(sackmat_m.stdbv(i, n))
		for j in range(i+1, n):
			ej = simple_tensor(sackmat_m.stdbv(j, n))
			for k in range(j+1, n):
				ek = simple_tensor(sackmat_m.stdbv(k, n))
				eijk = ei ^ ej ^ ek
				print "e" + str(i) + " ^ e" + str(j) + " ^ e" + str(k)
				eijk.printf()

	n = 4
	for i in range(0, n):
		ei = simple_tensor(sackmat_m.stdbv(i, n))
		for j in range(i+1, n):
			ej = simple_tensor(sackmat_m.stdbv(j, n))
			eij = ei ^ ej
			print "e" + str(i) + " ^ e" + str(j)
			eij.printf()

	n = 4
	for i in range(0, n):
		ei = simple_tensor(sackmat_m.stdbv(i, n))
		for j in range(i+1, n):
			ej = simple_tensor(sackmat_m.stdbv(j, n))
			for k in range(j+1, n):
				ek = simple_tensor(sackmat_m.stdbv(k, n))
				eijk = ei ^ ej ^ ek
				print "e" + str(i) + " ^ e" + str(j) + " ^ e" + str(k)
				eijk.printf()

	n = 4
	for i in range(0, n):
		ei = simple_tensor(sackmat_m.stdbv(i, n))
		for j in range(i+1, n):
			ej = simple_tensor(sackmat_m.stdbv(j, n))
			for k in range(j+1, n):
				ek = simple_tensor(sackmat_m.stdbv(k, n))
				for l in range(k+1, n):
				 	el = simple_tensor(sackmat_m.stdbv(l, n))
					eijkl = ei ^ ej ^ ek ^ el
					print "e" + str(i) + " ^ e" + str(j) + " ^ e" + str(k) + " ^ e" + str(l)
					eijkl.printf()

# ----------------------------------------------------------------
#import random
#
#def foobar():
#	#A = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
#	#A = [[[0, 1], [0, 0]], [[0, 0], [0, 0]]]
#	n=5
#	A = make_zero_3_tensor(n)
#
#	g = random.Random(1)
#	for i in range(0, n):
#		for j in range(0, n):
#			for k in range(0, n):
#				#A[i][j][k] = i*j*k+ i*i - j*k + 1
#				A[i][j][k] = g.random()
#
#
#	print_3_tensor(A)
#
#	#Z = make_zero_3_tensor(2)
#	#print_3_tensor(Z)
#
#	S = mksymm3(A)
#	print_3_tensor(S)
#
#	S = mkskew3(A)
#	print_3_tensor(S)
#
#foobar()

# ----------------------------------------------------------------
def apply_demo():

	#T = simple_tensor([[1,0],[0,1]])
	#u = [3,4]
	#v = [5,6]

	#T = simple_tensor([[1,0,0],[0,1,0],[0,0,1]])
	#u = [3,4,5]
	#v = [5,6,7]

	T = simple_tensor([[0,1,1],[-1,0,1],[-1,-1,0]])
	u = [3,4,5]
	v = [5,6,7]

	uv = simple_tensor(u) * simple_tensor(v)

	t = T.of([u,v])

	T.printf()
	uv.printf()
	print_row_vector(u)
	print
	print_row_vector(v)
	print

	print t

# ----------------------------------------------------------------
def symstuff():
	r = 3
	n = 3
	p = n ** r
	A = make_zero_simple_tensor(r, n)
	v = 1

	g = random.Random(1)
	for i in range(0, p):
		I = multidx(i, r, n)
		#A[I] = v
		A[I] = g.random()
		v += 1

	B = A.Alt()
	C = A.Sym()
	print "Orig:"; A.printf(); print
	print "Alt :"; B.printf(); print
	print "Sym :"; C.printf(); print
	D = A - B - C
	print "OAS :"; D.printf(); print

# ----------------------------------------------------------------
def cobtest():
	g = simple_tensor([[1,0],[0,1]])
	Q = sackmat([[2,0],[1,1]]).transpose()

	#g = simple_tensor([[1,0,0],[0,1,0],[0,0,1]])
	#Q = sackmat([[2,1,1],[0,1,2],[0,0,1]]).transpose()

	print "Q:"; Q.printf(); print
	print "g:"; g.printf(); print
	gp = g.cov_cob(Q); gp.printf()
	gp = g.ctv_cob(Q); gp.printf()
	gp = g.cob(Q,[1,0]); gp.printf()
	gp = g.cob(Q,[0,1]); gp.printf()


# ================================================================
#apply_demo()
symstuff()
#cobtest()
