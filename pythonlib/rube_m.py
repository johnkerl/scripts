# ================================================================
# RUBE.L / RUBE.PY
#
# Constructs the cycle decomposition of sequences of moves on the Rubik's Cube.
# Faces are denoted by F, R, B, L, U and D for front, right, back, left, up and
# down, respectively.  Corner pieces are denoted by their three faces, or
# 'elements', edges by their two.
#
# Moves are denoted by their face and either:
# (a)  +, -, or 2, for clockwise, counterclockwise and half-turn, or
# (b)  no suffix, -1 and 2, for CW, CCW and half-turn.
# The two notation styles for turns may be intermixed.
# Examples: U+, F-1, R2.
#
# Processes are given as a list of moves, e.g. '(U+ F-1 R2)'.
#
# John Kerl
# Written in Lisp 12/93
# Ported to Python 4/06
# kerl.john.r@gmail.com
# ================================================================

import sys

# -----------------------------------------------------------------------------
# RUBE EXPONENT SECTION

def invert_moves(proc):
	result = []
	for move in proc:
		result.append(invert_move(move))
	result.reverse()
	return result

def invert_move(move):
	return invert_move_table[move]

def power_of_sequence(moves, power):
	return moves * power

def conjugate(proc1, proc2):
	"""Returns the conjugate of A by B, i.e. A * B * A^-1."""
	return proc1 + proc2 + invert_moves(proc1)

def commutator (proc1, proc2):
	"""Returns the commutator of A and B, i.e. [A, B], i.e. A * B * A^-1 * B^-1."""
	return proc1 + proc2 + invert_moves(proc1) + invert_moves(proc2)

# -----------------------------------------------------------------------------
# RUBE PPRINT SECTION

def print_moves (moves):
	for move in moves:
		print move,
	print

def print_cycle_decomposition (moves):
	cycles = cycle_decomposition(moves)
	for cycle in cycles:
		print_cycle(cycle)

def print_cycle(cycle):
	for element in cycle:
		print element,
	print

def print_images (moves):
	pairs = images_of_all_pieces(moves)
	for pair in pairs:
		for element in pair:
			print element,
		print

# ================================================================
def tell_about(moves):
	validate_moves(moves)
	print "-- Sequence is:"
	print_moves(moves)
	print "-- Image is:"
	print_images(moves)
	print "-- Cycle decomposition is:"
	print_cycle_decomposition(moves)
	print "-- Order is:"
	print order(moves)
	print

# ----------------------------------------------------------------
# This is a handy keystroke-saver.
# Example:  'FR2B-L' -> ['F', 'R2', 'B-', 'L'].
def rube_unpack(packed):
	unpacked = []
	idx = 0
	ell = len(packed)
	while (idx < ell):
		move = packed[idx]
		if (idx + 1 < ell):
			if (packed[idx+1] == '+'):
				idx  += 1
				move += packed[idx]
			elif (packed[idx+1] == '-'):
				idx  += 1
				move += packed[idx]
			elif (packed[idx+1] == '2'):
				idx  += 1
				move += packed[idx]
		unpacked.append(move)
		idx += 1
	return unpacked

# ----------------------------------------------------------------
def validate_moves(moves):
	for move in moves:
		ok = True
		ell = len(move)
		if   (ell == 1):
			if move[0] not in 'FRBLUDfrblud':
				ok = False
		elif (ell == 2):
			if move[0] not in 'FRBLUDfrblud':
				ok = False
			if move[1] not in '+-2':
				ok = False
		else:
			ok = False
		if (not ok):
			print >> sys.stderr, "Malformed move \"%s\" in sequence \"%s\"." \
				% (move, moves)
			sys.exit(1)

# ================================================================
def images_of_all_pieces (moves):
	return images_of_pieces(moves, list_of_all_pieces)

def images_of_pieces (moves, pieces):
	images = moves_on_pieces(moves, pieces)
	result = []
	n = len(pieces)
	for i in range(0, n):
		piece = pieces[i]
		image = images[i]
		if (piece_equal(piece, image)):
			sign = sign_of_rotation(piece, image)
			if (sign != []):
				result.append([piece, image])
		else:
			result.append([piece, "->", image])
	return result

# ================================================================
def cycle_decomposition (moves):
	"""Given a list of Rubik's Cube pieces and a list of moves, return the cycle
	decomposition of the moves, omitting trivial cycles."""
	return delete_1_cycles(find_cycles(moves, list_of_all_pieces))

# ----------------------------------------------------------------
def order (moves):
	return multi_lcm(cycle_lengths(cycle_decomposition(moves)))

# ----------------------------------------------------------------
def multi_lcm(list):
	result = 1
	for element in list:
		result = lcm2(result, element)
	return result

# ----------------------------------------------------------------
def lcm2(a, b):
	return a * b / gcd2(a, b)

# ----------------------------------------------------------------
def gcd2(a, b):
	while b:
		a, b = b, a % b
	return a

# ----------------------------------------------------------------
def cycle_lengths (cycles):
	lengths = []
	for cycle in cycles:
		lengths.append(cycle_length(cycle))
	return lengths

# ----------------------------------------------------------------
def cycle_length (cycle):
	if (cycle[-1] == '+') or (cycle[-1] == '-'):
		if (len(cycle[0]) == 3):
			return 3 * (len(cycle) - 1)
		else:
			return 2 * (len(cycle) - 1)
	else:
		return len(cycle)

# ----------------------------------------------------------------
def delete_1_cycles (cycles):
	non_trivial_cycles = []
	for cycle in cycles:
		if (len(cycle) > 1):
			non_trivial_cycles.append(cycle)
	return non_trivial_cycles

# ----------------------------------------------------------------
def find_cycles (moves, pieces):
	cycles = []
	for piece in pieces:
		if (not in_cycle_list(piece, cycles)):
			cycles.append(find_cycle(moves, piece))
	return cycles

# ----------------------------------------------------------------
def in_cycle_list(piece, cycles):
	for cycle in cycles:
		for cycle_piece in cycle:
			if (piece_equal(piece, cycle_piece)):
				return True
	return False

# ----------------------------------------------------------------
def find_cycle (moves, piece):
	cycle = [piece]
	next = moves_on_piece(moves, piece)
	while (not piece_equal(piece, next)):
		cycle.append(next)
		next = moves_on_piece(moves, next)
	cycle += sign_of_rotation(piece, next)
	return cycle

# ================================================================
def sign_of_rotation (orient_1, orient_2):
	# Same representation of same piece -- no spin.
	if (orient_1 == orient_2):
		return []

	# No sign if pieces aren't the same.
	if (not piece_equal(orient_1, orient_2)):
		return []

	# Say + for any differently represented edges (since the
	# rotation group only has order 2).
	if (len(orient_1) ==2):
		return ["+"]

	# Now they must be corner pieces.  Do a table lookup.
	if (orient_1 in clockwise_orient_list):
		if (orient_1[1] == orient_2[0]):
			return ["+"]
		else:
			return ["-"]
	else:
		if (orient_1[1] == orient_2[0]):
			return ["-"]
		else:
			return ["+"]

# ================================================================
def moves_on_pieces (moves, pieces):
	result = []
	for piece in pieces:
		result.append(moves_on_piece(moves, piece))
	return result

# ----------------------------------------------------------------
def moves_on_piece (moves, piece):
	result = piece
	if (len(piece) == 3):
		for move in moves:
			result = move_on_corner_piece(move, result)
	if (len(piece) == 2):
		for move in moves:
			result = move_on_edge_piece(move, result)
	return result

# ================================================================
# Returns the image of a corner piece under a move.  Breaks the piece up into
# its component faces; looks up the image of each face under the specifed move,
# then puts the resulting faces back together.
#
# What the if-statement does is, if the move (denoted by a face) isn't on the
# same face as one of the piece's faces, then the piece is unaffected by the
# move.  E.g. URF is affected by F, but URL is not.

def move_on_corner_piece (move, corner):
	ps0  = corner[0]
	ps1  = corner[1]
	ps2  = corner[2]
	face = move[0]
	if (face == ps0) or (face == ps1) or (face == ps2):
		return move_on_face(move, ps0) \
			+  move_on_face(move, ps1) \
			+  move_on_face(move, ps2)
	else:
		return corner

# ----------------------------------------------------------------
# Returns the image of an edge piece under a move.  Breaks the piece up into
# its component faces; looks up the image of each face under the specifed move,
# then puts the resulting faces back together.
#
# What the if-statement does is: if the move (denoted by a face) isn't on the
# same face as one of the piece's faces, then the piece is unaffected by the
# move.  E.g. UF is affected by F, but UR is not.
#

def move_on_edge_piece (move, edge):
	ps0  = edge[0]
	ps1  = edge[1]
	face = move[0]
	if (face == ps0) or (face == ps1):
		return move_on_face(move, ps0) + move_on_face(move, ps1)
	else:
		return edge

# FRBLUD act trivially on centers.  Sfrblud move them.
# Need a separate table.

#def move_on_center_piece (move, center):
#	ps0  = center[0]
#	face = move[0]
#	if (face == ps0):
#		return move_on_face(move, ps0)
#	else:
#		return center

# ----------------------------------------------------------------
# Returns the image of a face under a move.
# Does a simple table lookup.

def move_on_face (move, face):
	return move_on_face_table[face][move]

# ================================================================
def piece_equal (piece_1, piece_2):
	"""The names of three adjacent faces provide the name of a corner piece;
	the names of two adjacent faces provide the name of an edge piece.
	However, a corner's three faces may be combined in any of six (3!) ways, e.g.
	URF, UFR, FRU, FUR, RFU, and RUF; and an edge's two faces may be combined
	in one of two (2!) ways, e.g. UF and FU.

	This function sees if two representations refer to the same piece.
	E.g. UFR is the same as FRU; UFR is not the same as UFL; UFR is not the
	same as UF."""

	length_1 = len(piece_1)
	length_2 = len(piece_2)

	if (length_1 != length_2):
		return False # Edges and corners can't possibly be the same.

	if (length_1 == 3):
		# Corner piece; there are 6 permutations of elts to consider.
		p11 = piece_1[0]
		p12 = piece_1[1]
		p13 = piece_1[2]
		p21 = piece_2[0]
		p22 = piece_2[1]
		p23 = piece_2[2]
		if   (p11 == p21) and (p12 == p22) and (p13 == p23):
			return True
		elif (p11 == p21) and (p12 == p23) and (p13 == p22):
			return True
		elif (p11 == p22) and (p12 == p21) and (p13 == p23):
			return True
		elif (p11 == p22) and (p12 == p23) and (p13 == p21):
			return True
		elif (p11 == p23) and (p12 == p21) and (p13 == p22):
			return True
		elif (p11 == p23) and (p12 == p22) and (p13 == p21):
			return True
		else:
			return False

	elif (length_1 == 2):
		# Edge piece; there are 2 permutation of elts to consider.
		p11 = piece_1[0]
		p12 = piece_1[1]
		p21 = piece_2[0]
		p22 = piece_2[1]

		if   (p11 == p21) and (p12 == p22):
			return True
		elif (p12 == p21) and (p11 == p22):
			return True
		else:
			return False

	else:
		print >> sys.stderr,  "piece_equal:  unrecognized input:", \
			piece_1, piece_2
		sys.exit(1)

# ================================================================
# LOOKUP TABLES

# ----------------------------------------------------------------
# The names of three adjacent faces provides the name of a corner piece.
# However, those three faces may be combined in any of six ways, e.g.  URF,
# UFR, FRU, FUR, RFU, and RUF.

# This variable contains all such names in which the faces are listed in a
# clockwise direction.  This could be calculated at run-time, but it seems
# simpler to do a table lookup.
clockwise_orient_list = [\
	"URF", "UFL", "ULB", "UBR", "DFR", "DRB", "DBL", "DLF" \
	"RFU", "FLU", "LBU", "BRU", "FRD", "RBD", "BLD", "LFD" \
	"FUR", "LUF", "BUL", "RUB", "RDF", "BDR", "LDB", "FDL"]

# ----------------------------------------------------------------
# Data for the image of a face under a move.

move_on_face_table = { \
	"F": { \
		"F":"F",  "R":"U",  "B":"F",  "L":"D",  "U":"L",  "D":"R",   \
		"F+":"F", "R+":"U", "B+":"F", "L+":"D", "U+":"L", "D+":"R",  \
		"F-":"F", "R-":"D", "B-":"F", "L-":"U", "U-":"R", "D-":"L",  \
		"F2":"F", "R2":"B", "B2":"F", "L2":"B", "U2":"B", "D2":"B"}, \
	"R": { \
		"F":"D",  "R":"R",  "B":"U",  "L":"R",  "U":"F",  "D":"B",   \
		"F+":"D", "R+":"R", "B+":"U", "L+":"R", "U+":"F", "D+":"B",  \
		"F-":"U", "R-":"R", "B-":"D", "L-":"R", "U-":"B", "D-":"F",  \
		"F2":"L", "R2":"R", "B2":"L", "L2":"R", "U2":"L", "D2":"L"}, \
	"B": { \
		"F":"B",  "R":"D",  "B":"B",  "L":"U",  "U":"R",  "D":"L",   \
		"F+":"B", "R+":"D", "B+":"B", "L+":"U", "U+":"R", "D+":"L",  \
		"F-":"B", "R-":"U", "B-":"B", "L-":"D", "U-":"L", "D-":"R",  \
		"F2":"B", "R2":"F", "B2":"B", "L2":"F", "U2":"F", "D2":"F"}, \
	"L": { \
		"F":"U",  "R":"L",  "B":"D",  "L":"L",  "U":"B",  "D":"F",   \
		"F+":"U", "R+":"L", "B+":"D", "L+":"L", "U+":"B", "D+":"F",  \
		"F-":"D", "R-":"L", "B-":"U", "L-":"L", "U-":"F", "D-":"B",  \
		"F2":"R", "R2":"L", "B2":"R", "L2":"L", "U2":"R", "D2":"R"}, \
	"U": { \
		"F":"R",  "R":"B",  "B":"L",  "L":"F",  "U":"U",  "D":"U",   \
		"F+":"R", "R+":"B", "B+":"L", "L+":"F", "U+":"U", "D+":"U",  \
		"F-":"L", "R-":"F", "B-":"R", "L-":"B", "U-":"U", "D-":"U",  \
		"F2":"D", "R2":"D", "B2":"D", "L2":"D", "U2":"U", "D2":"R"}, \
	"D": { \
		"F":"L",  "R":"F",  "B":"R",  "L":"B",  "U":"D",  "D":"D",   \
		"F+":"L", "R+":"F", "B+":"R", "L+":"B", "U+":"D", "D+":"D",  \
		"F-":"R", "R-":"B", "B-":"L", "L-":"F", "U-":"D", "D-":"D",  \
		"F2":"U", "R2":"U", "B2":"U", "L2":"U", "U2":"D", "D2":"D"}  \
	}
	# Include Sfrblud

#move_on_center_table = { \
#	"F": { \
#		"F":"F",  "R":"R",  "B":"B",  "L":"L",  "U":"U",  "D":"D",   \
#		"F+":"F", "R+":"R", "B+":"B", "L+":"L", "U+":"U", "D+":"D",  \
#		"F-":"F", "R-":"R", "B-":"B", "L-":"L", "U-":"U", "D-":"D",  \
#		"F2":"F", "R2":"R", "B2":"B", "L2":"L", "U2":"U", "D2":"D"}, \
#	"R": { \
#		"F":"F",  "R":"R",  "B":"B",  "L":"L",  "U":"U",  "D":"D",   \
#		"F+":"F", "R+":"R", "B+":"B", "L+":"L", "U+":"U", "D+":"D",  \
#		"F-":"F", "R-":"R", "B-":"B", "L-":"L", "U-":"U", "D-":"D",  \
#		"F2":"F", "R2":"R", "B2":"B", "L2":"L", "U2":"U", "D2":"D"}, \
#	"B": { \
#		"F":"F",  "R":"R",  "B":"B",  "L":"L",  "U":"U",  "D":"D",   \
#		"F+":"F", "R+":"R", "B+":"B", "L+":"L", "U+":"U", "D+":"D",  \
#		"F-":"F", "R-":"R", "B-":"B", "L-":"L", "U-":"U", "D-":"D",  \
#		"F2":"F", "R2":"R", "B2":"B", "L2":"L", "U2":"U", "D2":"D"}, \
#	"L": { \
#		"F":"F",  "R":"R",  "B":"B",  "L":"L",  "U":"U",  "D":"D",   \
#		"F+":"F", "R+":"R", "B+":"B", "L+":"L", "U+":"U", "D+":"D",  \
#		"F-":"F", "R-":"R", "B-":"B", "L-":"L", "U-":"U", "D-":"D",  \
#		"F2":"F", "R2":"R", "B2":"B", "L2":"L", "U2":"U", "D2":"D"}, \
#	"U": { \
#		"F":"F",  "R":"R",  "B":"B",  "L":"L",  "U":"U",  "D":"D",   \
#		"F+":"F", "R+":"R", "B+":"B", "L+":"L", "U+":"U", "D+":"D",  \
#		"F-":"F", "R-":"R", "B-":"B", "L-":"L", "U-":"U", "D-":"D",  \
#		"F2":"F", "R2":"R", "B2":"B", "L2":"L", "U2":"U", "D2":"D"}, \
#	"D": { \
#		"F":"F",  "R":"R",  "B":"B",  "L":"L",  "U":"U",  "D":"D",   \
#		"F+":"F", "R+":"R", "B+":"B", "L+":"L", "U+":"U", "D+":"D",  \
#		"F-":"F", "R-":"R", "B-":"B", "L-":"L", "U-":"U", "D-":"D",  \
#		"F2":"F", "R2":"R", "B2":"B", "L2":"L", "U2":"U", "D2":"D"}, \
	# Include Sfrblud

#	}

# ----------------------------------------------------------------
# A table to show the inverse of any move.
invert_move_table = { \
	"F+":"F-", "R+":"R-", "B+":"B-", "L+":"L-", "U+":"U-", "D+":"D-", \
	"F-":"F+", "R-":"R+", "B-":"B+", "L-":"L+", "U-":"U+", "D-":"D+", \
	"F2":"F2", "R2":"R2", "B2":"B2", "L2":"L2", "U2":"U2", "D2":"D2", \
	"F" :"F-", "R" :"R-", "B" :"B-", "L" :"L-", "U" :"U-", "D" :"D-", \
	"F-":"F",  "R-":"R",  "B-":"B",  "L-":"L",  "U-":"U",  "D-":"D",  \
	}

	#"S-":"S",  "S-":"S", "S2":"S2",
	#"f+":"f-", "r+":"r-", "b+":"b-", "l+":"l-", "u+":"u-", "d+":"d-", \
	#"f-":"f+", "r-":"r+", "b-":"b+", "l-":"l+", "u-":"u+", "d-":"d+", \
	#"f2":"f2", "r2":"r2", "b2":"b2", "l2":"l2", "u2":"u2", "d2":"d2", \
	#"f" :"f-", "r" :"r-", "b" :"b-", "l" :"l-", "u" :"u-", "d" :"d-", \
	#"f-":"f",  "r-":"r",  "b-":"b",  "l-":"l",  "u-":"u",  "d-":"d",  \

	# Include S, f, r, b, l, u, d

# ----------------------------------------------------------------
# A table of all the movable pieces (i.e., not including centers)
# on the cube.
list_of_all_pieces = [ \
	"UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBL", "DBR", \
	"UF", "UL", "UB", "UR", "FR", "FL", "BL", "BR", "DF", "DL", "DB", "DR"]
	# Centers:
	# "F", "R", "B", "L", "U", "D"
