#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
from math import *
from sackmat_m import *
import copy

# ----------------------------------------------------------------
# Let
#   F: R^m -> R^n
# i.e.
#          [ F_1(x_1, ..., x_m) ]
#   F(x) = [ :   :         :    ]
#          [ F_n(x_1, ..., x_m) ].
# Then Dij = dFi/dxj, i=1..n, j=1..m (an n x m matrix).
# This is numerically approximated (forward-difference approximation) by
#   (F(x1,...,xj+h,...,xn) - F(x1,...,xj,...,xn)) / h
# or (centered-difference approximation)
#   (F(x1,...,xj+h/2,...,xn) - F(x1,...,xj-h/2,...,xn)) / h.

def jac(F, q, h=1e-6):
	m = len(q)
	n = len(F(q))
	DFq = make_zero_matrix(n, m)
	# Centered-difference approximation
	h2 = 0.5 * h
	for j in range(0, m):
		qb = copy.copy(q)
		qf = copy.copy(q)
		qb[j] -= h2
		qf[j] += h2
		Fqb = F(qb)
		Fqf = F(qf)
		for i in range(0, n):
			DFq[i][j] = (Fqf[i] - Fqb[i]) / h
	return DFq

# ----------------------------------------------------------------
def F1(q):
	[x, y, z] = q

	#f1 = x**2
	#f2 = y**2
	#f3 = z**2

	#f1 = x**2 * y**2
	#f2 = y**2 * z**2
	#f3 = z**2 * x**2

	f1 = x * y
	f2 = y * z
	f3 = z * x

	#f1 = 1.0 * y * y
	#f2 = 2.0 * x
	#f3 = 3.0 * z

	return [f1, f2, f3]

# ----------------------------------------------------------------
def F2(q):
	[x, y, z] = q
	return [x**2 + y**2 + z**2]

# ----------------------------------------------------------------
def do_point(F,q):
	print "q =", q
	DFq = jac(F, q)
	print "DFq="
	print DFq
	#print "det(DFq) =", DFq.det()

# ----------------------------------------------------------------
def do_point_with_det(F,q):
	print "-" * 40
	print "q =", q
	DFq = jac(F, q)
	print "DFq="
	print DFq
	print "det(DFq) =", DFq.det()

# ----------------------------------------------------------------
def frufru():
	F = F1
	do_point_with_det(F, [0,0,0])
	print

	do_point_with_det(F, [0,0,1])
	do_point_with_det(F, [0,1,0])
	do_point_with_det(F, [1,0,0])
	print

	do_point_with_det(F, [1,1,0])
	do_point_with_det(F, [1,0,1])
	do_point_with_det(F, [0,1,1])
	print

	do_point_with_det(F, [1,1,1])
	do_point_with_det(F, [1,2,3])
	do_point_with_det(F, [sqrt(0.5),sqrt(0.5),0])
	a=0.1
	do_point_with_det(F, [cos(a),sin(a),0])

	a = 0.2
	b = 0.3
	c = sqrt(1 - a**2 - b**2)
	do_point_with_det(F, [a,b,c])

	a = 0.8
	b = 0.2
	c = sqrt(1 - a**2 - b**2)
	do_point_with_det(F, [a,b,c])

	print

# ----------------------------------------------------------------
def F(q):
	[x, y, z] = q

	#f1 = x**2
	#f2 = y**2
	#f3 = z**2

	#f1 = x**2 * y**2
	#f2 = y**2 * z**2
	#f3 = z**2 * x**2

	f1 = x * y
	f2 = y * z
	f3 = z * x

	#f1 = 1.0 * y * y
	#f2 = 2.0 * x
	#f3 = 3.0 * z

	return [f1, f2, f3]

# ----------------------------------------------------------------
def G(q):
	[x, y, z] = q
	return [x**2 + y**2 + z**2]

# ----------------------------------------------------------------
def gt_something():
	thetalo = 0
	thetahi = 2*math.pi
	philo = 0
	phihi = math.pi

	nphi   = 12
	ntheta = 12

	if (len(sys.argv) == 3):
		nphi   = int(sys.argv[1])
		ntheta = int(sys.argv[2])
	dtheta = (thetahi-thetalo)/ntheta
	dphi   = (phihi-philo)/nphi

	phi = 0
	for ii in range(0, nphi):
		theta = 0
		for jj in range(0, ntheta):
			x = sin(phi) * cos(theta)
			y = sin(phi) * sin(theta)
			z = cos(phi)
			q = [x,y,z]

			DF = jac(F, q)
			d = DF.det()

			# Let G(x,y,z) = x^2 + y^2 + z^2.  The unit sphere is the level set
			# for G(x,y,z) = 1.
			# Tangent plane at (u,v,w):
			#   dG/dx(x-u) + dG/dy(y-v) + dG/dz(z-w)
			# where (u,v,w) are the coordinates of the point q and (x,y,z) are variable.
			DG = jac(G, q)

			# For DF restricted to this tangent plane:
			# * DG (i.e. grad G) is the normal vector
			# * This gives a point-normal form for the tangent plane
			# * Project the standard basis for R3 onto the tangent plane
			# * Row-reduce

			DF = jac(F, q)
			# * Form an orthonormal basis
			# * Compute DF of the basis
			# * Row-reduce that to get the rank of DF on TM|q

			#print "q = ", q,
			#print "det(DF) = ", d
			#print "%7.4f %7.4f %7.4f   %7.4f   %7.4f,%7.4f %7.4f,%7.4f %7.4f,%7.4f" % (
			#	x,y,z, d, DG[0][0], -DG[0][0]*x, DG[0][1], -DG[0][1]*y, DG[0][2], -DG[0][2]*z)

			nx = DG[0][0]
			ny = DG[0][1]
			nz = DG[0][2]
			nml = [nx, ny, nz]

			e0 = [1,0,0]
			e1 = [0,1,0]
			e2 = [0,0,1]

			# Project the standard basis for R3 down to the tangent plane TM|q.
			proj_e0 = projperp(e0, nml)
			proj_e1 = projperp(e1, nml)
			proj_e2 = projperp(e2, nml)
			proj_e  = sackmat([proj_e0, proj_e1, proj_e2])

			# Row-reduce, compute rank, and trim
			proj_e.row_echelon_form()
			rank = proj_e.rank_rr()
			proj_e.elements = proj_e.elements[0:rank]

			# Orthonormalize
			proj_e = gram_schmidt(proj_e)

			#print "q=[%7.4f,%7.4f,%7.4f]" % (x, y, z),
			#print "nml=[%7.4f,%7.4f,%7.4f]" % (nx, ny, nz),
			#print "p0=[%7.4f,%7.4f,%7.4f] p1=[%7.4f,%7.4f,%7.4f]" % (
				#proj_e[0][0], proj_e[0][1], proj_e[0][2], proj_e[1][0], proj_e[1][1], proj_e[1][2]),

			# Take DF of the orthonormal basis.
			proj_e = proj_e.transpose()
			proj_e = DF * proj_e
			proj_e = proj_e.transpose()
			rank   = proj_e.rank()

			#print "p0=[%7.4f,%7.4f,%7.4f] p1=[%7.4f,%7.4f,%7.4f]" % (
				#proj_e[0][0], proj_e[0][1], proj_e[0][2], proj_e[1][0], proj_e[1][1], proj_e[1][2]),

			#print "rank=", proj_e.rank_rr(),
			#print "d=%11.3e" % (d),

			# xxx hack
			if (rank == 1):
				d = 0.7
			#print "%11.3e" % (d),
			print "%8.4f" % (d),

			#print
			theta += dtheta
		print
		phi += dphi
gt_something()
