#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from sackmat_m import *

# ----------------------------------------------------------------
def test_submx_premul():
	A = sackmat([
		[1,2,3],
		[4,5,6],
		[7,8,9]])
	Q = sackmat([
		[0,1],
		[1,0]])
	[sr, ar] = [1, 1]

	Q.printp("Q")
	A.printp("Old A")
	A.premultiply_by_submatrix(Q, sr, ar)
	A.printp("New A")

# ----------------------------------------------------------------
def test_submx_postmul():

	A = sackmat([
		[1,2,3],
		[4,5,6],
		[7,8,9]])
	Q = sackmat([
		[0,1],
		[1,0]])
	sc = 1

	Q.printp("Q")
	A.printp("Old A")
	A.postmultiply_by_submatrix_transpose(Q, sc)
	A.printp("New A")

# ----------------------------------------------------------------
def test_tip():
	A = sackmat([
		[1,2,3],
		[4,5,6],
		[7,8,9]])
	A.printp("A")
	A.transpose_in_place()
	A.printp("A^t")

# ----------------------------------------------------------------
def test_mk_seq():
	A = make_seq_matrix(1,1); A.printp("seq")
	A = make_seq_matrix(2,2); A.printp("seq")
	A = make_seq_matrix(3,3); A.printp("seq")
	A = make_seq_matrix(4,4); A.printp("seq")

	A = make_nseq_matrix(1,1); A.printp("nseq")
	A = make_nseq_matrix(2,2); A.printp("nseq")
	A = make_nseq_matrix(3,3); A.printp("nseq")
	A = make_nseq_matrix(4,4); A.printp("nseq")

# ----------------------------------------------------------------
def test_qr():
	#A = sackmat([[1,2],[3,4]])
	#A = sackmat([
	#	[3,0,0],
	#	[4,1,0],
	#	[0,0,1]])
	A = sackmat([
		[-1,2,3],
		[4,-5,6],
		[7,8,-9]])
	[nr,nc] = A.dims()
	Q = make_zero_matrix(nr,nr)
	R = make_zero_matrix(nr,nc)
	A.QR_decomp(Q,R)
	QR = Q*R

	A.printp("A")
	Q.printp("Q")
	R.printp("R")
	QR.printp("QR")

# ----------------------------------------------------------------
#test_submx_premul()
#test_submx_postmul()
#test_tip()
#test_mk_seq()
test_qr()
