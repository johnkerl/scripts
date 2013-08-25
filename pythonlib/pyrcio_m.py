#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2005-06-08
#
# Some simple I/O routines for real and complex scalars, vectors,
# and matrices.
# ================================================================

from __future__ import division # 1/2 = 0.5, not 0.
import sys
import copy
import re

# ================================================================
def complex_scalar_from_string(orig_line, lno):
	zre = 0
	zim = 0
	line = copy.copy(orig_line)

	# Chomp trailing newline, if any.
	if (line[-1] == '\n'):
		line = line[0:-1]

	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	if (line == ""):
		print >> sys.stderr, "pyrcio_m:  empty input at line", lno
		sys.exit(1)

	# Tokenize.
	strings = re.split(r"\s+", line)

	if (len(strings) == 2):
		zre = float(strings[0])
		zim = float(strings[1])
	elif (len(strings) == 1):
		zre = float(strings[0])
	else:
		print >> sys.stderr, "pyrcio_m:  unrecognizable input at line", lno
		sys.exit(1)

	return zre + zim*1j

# ----------------------------------------------------------------
def real_scalar_from_string(orig_line, lno):
	z = 0
	line = copy.copy(orig_line)

	# Chomp trailing newline, if any.
	if (line[-1] == '\n'):
		line = line[0:-1]

	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	if (line == ""):
		print >> sys.stderr, "pyrcio_m:  empty input at line", lno
		sys.exit(1)

	# Tokenize.
	strings = re.split(r"\s+", line)

	if (len(strings) == 1):
		z = float(strings[0])
	else:
		print >> sys.stderr, "pyrcio_m:  unrecognizable input at line", lno
		sys.exit(1)

	return z


# ================================================================
def read_complex_column_vector(file_name = "-"):
	n = 0
	v = []
	lno = 0

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	while (1):
		line = file_handle.readline()
		if (line == ""):
			break

		lno += 1
		v.append(complex_scalar_from_string(line, lno))
		n += 1

	if (file_name != "-"):
		file_handle.close()

	if (n == 0):
		print >> sys.stderr, "pyrcio_m:  Empty input."
		sys.exit(1)
	return v

# ----------------------------------------------------------------
def read_real_column_vector(file_name = "-"):
	n = 0
	v = []
	lno = 0

	if (file_name == "-"):
		file_handle = sys.stdin
	else:
		try:
			file_handle = open(file_name, 'r')
		except:
			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
			sys.exit(1)

	while (1):
		line = file_handle.readline()
		if (line == ""):
			break

		lno += 1
		v.append(real_scalar_from_string(line, lno))
		n += 1

	if (file_name != "-"):
		file_handle.close()

	if (n == 0):
		print >> sys.stderr, "pyrcio_m:  Empty input."
		sys.exit(1)
	return v

# ----------------------------------------------------------------
def print_complex_column_vector(v):
	n = len(v)
	for i in range(0, n):
		print "%18.11f %18.11f" % (v[i].real, v[i].imag)

# ----------------------------------------------------------------
def print_real_column_vector(v):
	n = len(v)
	for i in range(0, n):
		print "%18.11f" % (v[i])


# ================================================================
def complex_row_vector_from_string(orig_line, lno):
	v = []
	line = copy.copy(orig_line)

	# Chomp trailing newline, if any.
	if (line[-1] == '\n'):
		line = line[0:-1]

	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	if (line == ""):
		print >> sys.stderr, "pyrcio_m:  empty input at line", lno
		sys.exit(1)

	# Tokenize.
	strings = re.split(r"\s+", line)

	if ((len(strings) % 2) == 1):
		print >> sys.stderr, "pyrcio_m:  odd complex input at line", lno
		sys.exit(1)
	ncplx = len(strings) / 2
	j = 0
	for i in range(0, ncplx):
		v.append(complex(float(strings[j]), float(strings[j+1])))
		j += 2

	return v

# ----------------------------------------------------------------
def real_row_vector_from_string(orig_line, lno):
	v = []
	line = copy.copy(orig_line)

	# Chomp trailing newline, if any.
	if (line[-1] == '\n'):
		line = line[0:-1]

	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	if (line == ""):
		print >> sys.stderr, "pyrcio_m:  empty input at line", lno
		sys.exit(1)

	# Tokenize.
	strings = re.split(r"\s+", line)

	j = 0
	for i in range(0, len(strings)):
		v.append(float(strings[j]))
		j += 1

	return v


# ================================================================
def validate_matrix(A):
	nr = len(A)
	min_nc = len(A[0])
	max_nc = 0
	for i in range(0, nr):
		cur_nc = len(A[i])
		if (cur_nc < min_nc):
			min_nc = cur_nc
		if (cur_nc > max_nc):
			max_nc = cur_nc
	if (min_nc != max_nc):
		print >> sys.stderr, "pyrcio_m:  ragged matrix."
		sys.exit(1)
	return max_nc

# ================================================================
def read_complex_matrix(file_name = "-"):
 	nr = 0
 	nc = 0
 	A = []
 	lno = 0

 	if (file_name == "-"):
 		file_handle = sys.stdin
 	else:
 		try:
 			file_handle = open(file_name, 'r')
 		except:
 			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
 			sys.exit(1)

 	while (1):
 		line = file_handle.readline()
 		if (line == ""):
 			break
 		lno += 1
 		A.append(complex_row_vector_from_string(line, lno))
 		nr += 1
	nc = validate_matrix(A)
 	if (file_name != "-"):
 		file_handle.close()

 	if ((nr == 0) or (nc == 0)):
 		print >> sys.stderr, "pyrcio_m:  Empty input."
 		sys.exit(1)
	return A

# ----------------------------------------------------------------
def read_real_matrix(file_name = "-"):
 	nr = 0
 	nc = 0
 	A = []
 	lno = 0

 	if (file_name == "-"):
 		file_handle = sys.stdin
 	else:
 		try:
 			file_handle = open(file_name, 'r')
 		except:
 			print >> sys.stderr, "Couldn't open \"" + file_name + "\" for read."
 			sys.exit(1)

 	while (1):
 		line = file_handle.readline()
 		if (line == ""):
 			break
 		lno += 1
 		A.append(real_row_vector_from_string(line, lno))
 		nr += 1
	nc = validate_matrix(A)
 	if (file_name != "-"):
 		file_handle.close()

 	if ((nr == 0) or (nc == 0)):
 		print >> sys.stderr, "pyrcio_m:  Empty input."
 		sys.exit(1)
	validate_matrix(A)
	return A

# ----------------------------------------------------------------
def print_complex_matrix(A):
	nr = len(A)
	nc = len(A[0])
	for i in range(0, nr):
		for j in range(0, nc):
			print "%11.7f %11.7f" % (A[i][j].real, A[i][j].imag),
		print

# ----------------------------------------------------------------
def print_real_matrix(A):
	nr = len(A)
	nc = len(A[0])
	for i in range(0, nr):
		for j in range(0, nc):
			print "%11.7f" % (A[i][j]),
		print
