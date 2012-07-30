
# ================================================================
# This software is released under the terms of the GNU GPL.
# Please see LICENSE.txt in the same directory as this file.
# John Kerl
# kerl.john.r@gmail.com
# 2007-05-31
# ================================================================

from sackset   import *
from sacktuple import *
from sackcoset import *

# ----------------------------------------------------------------
def sackexp(x, n):
	# Naive for now; binary exp'n later
	if (n <= 0):
		print "sackexp:  can't do non-positive exponent", n
		sys.exit(1)
	y = x
	while (n > 1):
		y = y * x
		n -= 1
	return y

# ----------------------------------------------------------------
def commutator(x, y):
	return x * y * x.inv() * y.inv()

# ----------------------------------------------------------------
def print_cayley_table(G):
	for a in G:
		for b in G:
			c = a*b
			print c,
		print 

# ----------------------------------------------------------------
def get_conj_classes(G):
	n = len(G)

	# Precompute a list of inverses
	Ginvs = []
	for g in G:
		Ginvs.append(g.inv())

	classes = []
	marks   = [0] * n
	for i in range(0, n):
		if (marks[i] == 1):
			continue

		a = G[i]
		cl_a = []
		for j in range(0, n):
			b = G[j] * a * Ginvs[j]
			marks[G.index(b)] = 1
			set_append_unique(cl_a, b)
		classes.append(cl_a)

	return classes

# ----------------------------------------------------------------
def get_conj_class_reps(G):
	classes = get_conj_classes(G)
	reps = []
	for cl in classes:
		reps.append(cl[0])
	return reps

# ----------------------------------------------------------------
def print_conj_classes(G):
	classes = get_conj_classes(G)
	for cl in classes:
		for g in cl:
			print g,
		print

# ----------------------------------------------------------------
def find_id(G):
	for e in G:
		is_id = 1
		for x in G:
			ex = e * x
			xe = x * e
			if (xe != x):
				is_id = 0
				break
			if (ex != x):
				is_id = 0
				break
		if (is_id):
			return [1, e]
	return [0, 0]

# ----------------------------------------------------------------
def get_order(x):
	xp = x * x
	k = 2
	while (1):
		if (xp == x):
			return k-1
		xp *= x
		k += 1
	return 0

# ----------------------------------------------------------------
def get_cycsgr(x):
	k = get_order(x)
	e = sackexp(x, k)
	cycsgr = range(0, k)
	xp = e
	for i in range(0, k):
		cycsgr[i] = xp
		xp *= x
	return cycsgr

# ----------------------------------------------------------------
def get_max_order(G):
	max_order = 0
	for x in G:
		k = get_order(x)
		if (k > max_order):
			max_order = k
	return max_order

# ----------------------------------------------------------------
def get_orders(G):
	orders = []
	for x in G:
		orders.append(get_order(x))
	return orders

# ----------------------------------------------------------------
def get_center(G):
	Z = []
	for a in G:
		a_in_center = 1
		for b in G:
			ab = a * b
			ba = b * a
			if not (ab == ba):
				a_in_center = 0
				break
		if (a_in_center):
			Z.append(a)
	return Z

# ----------------------------------------------------------------
def close_group(G):
	while (1):
		n = len(G)
		#print "... n=", n # xxx temp
		for i in range(0, n):
			x = G[i]
			for j in range(0, n):
				y = G[j]
				xy = x * y
				yx = y * x
				set_append_unique(G, xy)
				set_append_unique(G, yx)
		if (len(G) == n):
			return 
				
# ----------------------------------------------------------------
def is_group(G):
	if (not is_closed(G)):
		#print "not closed"
		return 0
	if (not is_associative(G)):
		#print "not assoc"
		return 0
	if (not has_unique_id(G)):
		#print "not unique id"
		return 0
	if (not has_inverses(G)):
		#print "not invs"
		return 0
	return 1

# ----------------------------------------------------------------
def is_closed(G):
	for x in G:
		for y in G:
			xy = x * y
			if (not element_of(xy, G)):
				return 0
	return 1

# ----------------------------------------------------------------
def is_associative(G):
	for a in G:
		for b in G:
			ab = a * b
			for c in G:
				bc = b * c
				ab_c = ab * c
				a_bc = a * bc
				if (ab_c != a_bc):
					#print "not assoc:", a, b, c
					return 0
	return 1

# ----------------------------------------------------------------
def has_unique_id(G):
	num_ids = 0
	for e in G:
		is_id = 1
		for x in G:
			ex = e * x
			xe = x * e
			if (xe != x):
				is_id = 0
				break
			if (ex != x):
				is_id = 0
				break
		if (is_id):
			num_ids += 1
	if (num_ids == 1):
		return 1
	else:
		return 0

# ----------------------------------------------------------------
def has_inverses(G):
	[found, e] = find_id(G)
	if (not found):
		return 0
	for x in G:
		x_has_inv = 0
		for y in G:
			xy = x * y
			yx = y * x
			if (xy == e) and (yx == e):
				x_has_inv = 1
				break
		if (not x_has_inv):
			return 0
	return 1

# ----------------------------------------------------------------
def is_cyclic(G):
	n = len(G)
	for a in G:
		k = get_order(a)
		if (k == n):
			return 1
	return 0

# ----------------------------------------------------------------
def is_abelian(G):
	Z = []
	for a in G:
		a_in_center = 1
		for b in G:
			ab = a * b
			ba = b * a
			if (ab != ba):
				return 0
	return 1

# ----------------------------------------------------------------
def nilbracket(G, Gi):
	G2 = []
	for a in G:
		for b in Gi:
			set_append_unique(G2, commutator(a, b))
	close_group(G2)
	return G2

# ----------------------------------------------------------------
def is_nilpotent(G):
	verbose = 1
	if (verbose):
		print "nilp check"
		print "Gp ",
		print_set_as_row(G)
		print
	Gp = copy.copy(G)
	while (1):
		Gpp = nilbracket(G,Gp)

		if (verbose):
			#print "gp: ",
			#print_set_as_row(Gp)
			print "gpp:",
			print_set_as_row(Gpp)
			print

		np  = len(Gp)
		npp = len(Gpp)
		if (npp == 1):
			return 1
		if (np == npp):
			return 0
		Gp = Gpp

# ----------------------------------------------------------------
def derived_subgroup(G):
	G1 = []
	for a in G:
		for b in G:
			set_append_unique(G1, commutator(a, b))
	close_group(G1)
	return G1

# ----------------------------------------------------------------
def is_solvable(G):
	verbose = 1
	if (verbose):
		print "slv check"
		print "Gp ",
		print_set_as_row(G)
		print
	Gp = copy.copy(G)
	while (1):
		Gpp = derived_subgroup(Gp)

		if (verbose):
			#print "gp: ",
			#print_set_as_row(Gp)
			print "gpp:",
			print_set_as_row(Gpp)
			print

		np  = len(Gp)
		npp = len(Gpp)
		if (npp == 1):
			return 1
		if (np == npp):
			return 0
		Gp = Gpp

# ----------------------------------------------------------------
def direct_product(G1, G2):
	n1 = len(G1)
	n2 = len(G2)
	n3 = n1 * n2
	G3 = range(0, n3)
	k = 0
	for i in range(0, n1):
		for j in range(0, n2):
			G3[k] = tuple([G1[i], G2[j]])
			k += 1
	return G3

# ----------------------------------------------------------------
# xxx direction argument: left or right
#def make_cosets(G, H):
#	return 0

def quotient(G, H):
	oG = len(G)
	oH = len(H)
	if ((oG % oH) != 0):
		print "quotient:  |H| (" + str(oG) + ") must divide |G| (" + str(oH) + ")."
		raise RuntimeError
	iGH = oG / oH
	if (iGH == 0):
		print "Empty quotient: |H| = " + str(oG) + ", |G| = " + str(oH) + "."
		raise RuntimeError

	GH = []
	for g in G:
		gHe = range(0, oH)
		for j in range(0, oH):
			gHe[j] = g * H[j]
		gH = coset(gHe)
		set_append_unique(GH, gH)

	return GH

# ----------------------------------------------------------------
# conj cls:

#	for i in range(0, n):
#		marks[i] = 0
#
#	for i in range(0, n):
#		if (marks[i])
#			continue
#		g = G[i]
#
#		nconj = 0
#		for x in G:
#			xinv = x.inv()
#			xg = x*g
#			xgxinv = g * xinv
#
#			// xxx really need an add-to-set lib function.
#			found = 0
#			for k in range(0, nconj):
#				pc = VARRAY_ELEMENT(pconjs, k,
#					pgroup->pspec->element_size)
#				if c == xgxinv:
#					found = 1
#					break
#			if (!found):
#				pc = VARRAY_ELEMENT(pconjs, nconj,
#					pgroup->pspec->element_size)
#				c = xgxinv
#
#				if (!group_find_index(pgroup, xgxinv,&cjgidx)):
#					fprintf(stderr,
#					"list_conj_cls:  group not closed.\n")
#					exit(1)
#				marks[cjgidx] = 1
#				nconj++
#
#		for (j = 0 j < nconj; j++):
#			pc = VARRAY_ELEMENT(pconjs, j, pgroup->pspec->element_size)
#			pgroup->pspec->pvprint(pc, pgroup->pvaux)
#
#		printf("\n")
