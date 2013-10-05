#!/usr/bin/python -Wall

# ================================================================
# These are routines for reading tabular data from files.  In particular, I use
# these for my data-plotting utilities, in conjunction with pylab.
#
# John Kerl
# kerl.john.r@gmail.com
# 2008-04-13
# ================================================================

import sys, re, time, datetime

# ----------------------------------------------------------------
def open_file_or_die(file_name, mode):
	if (file_name == "-"):
		if mode == 'r':
			file_handle = sys.stdin
		else:
			file_handle = sys.stdout
	else:
		try:
			file_handle = open(file_name, mode)
		except:
			print >> sys.stderr, \
				"Couldn't open file \"%s\" for mode \"%s\"." \
				% (file_name, mode)
			sys.exit(1)
	return file_handle

# ----------------------------------------------------------------
def text_columns_from_file(file_name, split_on_comma=False):
	"""Given an input file containing tabular data, returns a list of columns.
	Pound signs may be used as comments; blank lines are skipped.
	For example, if the input file is

	1 2 3
	4 5 6 # Comment here

	7 8 9
	a b c

	then this routine returns
	[['1', '4', '7', 'a'], ['2', '5', '8', 'b'], ['3', '6', '9', 'c']].
	"""

	file_handle = open_file_or_die(file_name, 'r')

	columns     = []
	num_fields  = -1
	line_number =  0

	while 1:
		line = file_handle.readline()
		if (line == ""):
			break
		line_number += 1

		# Skip the header, which for CSV format needn't begin with a #.
		if split_on_comma == True and line_number == 1:
			continue

		# Strip trailing carriage return, if any.
		if line[-1] == '\n':
			line = line[0:-1]
		# Strip comments.
		line = re.sub(r"#.*",  r"", line)
		# Strip leading and trailing whitespace.
		line = re.sub(r"^\s+", r"", line)
		line = re.sub(r"\s+$", r"", line)
		# Skip blank lines.
		if re.match(r"^$", line):
			continue

		# Split on comma or whitespace.
		if split_on_comma:
			fields = line.split(',')
		else:
			fields = line.split()
		curr_num_fields = len(fields)

		if (num_fields == -1):
			# First data line of file.
			num_fields = curr_num_fields
			for j in range(0, num_fields):
				columns.append([])
		elif curr_num_fields != num_fields:
			print >> sys.stderr, "Ragged input in file \"%s\" at line %d." % \
				(file_name, line_number)
			sys.exit(1)
		for j in range(0, num_fields):
			columns[j].append(fields[j])

	if (file_name != "-"):
		file_handle.close()

	return columns

# ----------------------------------------------------------------
def float_columns_from_file(file_name, split_on_comma=False):
	"""Given an input file containing float tabular data, returns a list of columns.
	Pound signs may be used as comments; blank lines are skipped.
	For example, if the input file is

	1 2 3
	4 5 6 # Comment here

	7 8 9

	then this routine returns
	[[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]
	"""

	columns = text_columns_from_file(file_name, split_on_comma)

	# # jrk 2011-03-21: column labels already read ...

	# # Skip the first line, if it looks like it's text (column labels).
	# try:
	# 	x = double(columns[0][0])
	# except:
	# 	columns = map(lambda column : column[1:], columns)

	num_rows = len(columns)
	num_cols = len(columns[0])
	for i in range(0, num_rows):
		for j in range(0, num_cols):
			entry = columns[i][j]
			if entry == '_':
				columns[i][j] = None
			elif entry == '':
				columns[i][j] = None
			else:
				columns[i][j] = float(entry)
	return columns

# ----------------------------------------------------------------
# Try accept various date formats, e.g.
#   20090102 14:30:00          20090102 14:30:00 +0000
#   20090102 14:30:00.000      20090102 14:30:00.000 +0000
#   20090102-14:30:00          20090102-14:30:00 +0000
#   20090102-14:30:00.000      20090102-14:30:00.000 +0000
# See http://docs.python.org/library/time.html for information about
# format strings.

# pylab dates are (floating-point) number of dates since 1/1 of 1 A.D.

def time_string_to_pylab_float_time(string):

	# I don't want this entire module to be dependent on pylab.
	try:
		import pylab
	except:
		print >> sys.stderr, "Couldn't import pylab module."
		sys.exit(1)

	# strptime can't handle the fractional part.  Split that off.
	pieces = string.split('.')
	date_and_time_part = pieces[0]
	time_struct = date_and_time_part_to_time_struct(date_and_time_part)
	float_time = pylab.date2num(time_struct)

	# Add in the fractional part.  Also try to handle the timezone part,
	# if any.
	if len(pieces) > 1:
		remaining_pieces = pieces[1].split()
		if len(remaining_pieces) == 1:
		    pass # No timezone offset
		elif len(remaining_pieces) == 2:
		    pass # Timezone offset; ignore it.
		else:
		    print >> sys.stderr, "Extra stuff in time string ", string
		    sys.exit(1)
		sec_frac = float('.' + remaining_pieces[0])
		return float_time + sec_frac / 24 / 60 / 60
	else:
		return float_time

def date_and_time_part_to_time_struct(date_and_time_part):
	fmts = ['%Y%m%d %H:%M:%S', '%Y-%m-%d %H:%M:%S',
		'%Y%m%d-%H:%M:%S', '%Y-%m-%d-%H:%M:%S',
		'%Y%m%d-%H%M%S', '%Y%m%d', '%Y-%m-%d']
	for fmt in fmts:
		try:
			time_struct = datetime.datetime.strptime(date_and_time_part, fmt)
			return time_struct
		except:
			pass

	print >> sys.stderr, "Couldn't parse \"%s\" as date." % (date_and_time_part)
	print >> sys.stderr, "Tried formats:",
	for fmt in fmts:
		print >> sys.stderr, fmt,
	print
	sys.exit(1)

# ----------------------------------------------------------------
def float_or_time_columns_from_file(file_name, which_are_time, split_on_comma=False):
	"""Given an input file containing float tabular data, returns a list of columns.
	Pound signs may be used as comments; blank lines are skipped.
	For example, if the input file is

	1 2 3
	4 5 6 # Comment here

	7 8 9

	then this routine returns
	[[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]
	"""

	columns = text_columns_from_file(file_name, split_on_comma)

	# Skip the first line, if it looks like it's text (column labels).
	try:
		x = double(columns[0][0])
	except:
		columns = map(lambda column : column[1:], columns)

	if   which_are_time == 'col0':
    		is_time_column_tester = lambda x : x == 0
	elif which_are_time == 'xyxy':
    		is_time_column_tester = lambda x : (x & 1) == 0
	else:
		print >> sys.stderr, \
			"float_or_time_columns_from_file:  which_are_time argument " \
			+ "must be \"col0\" or \"xyxy\"; got \"%s\"." % (which_are_time)
		sys.exit(1)

	num_cols = len(columns)
	num_rows = len(columns[0])
	for j in range(0, num_cols):
		for i in range(0, num_rows):
			entry = columns[j][i]
			if entry == '_' or entry == '':
				columns[j][i] = None
			elif is_time_column_tester(j):
				columns[j][i] = time_string_to_pylab_float_time(entry)
			else:
				columns[j][i] = float(entry)
	return columns

# ----------------------------------------------------------------
def xy_columns_from_file(file_name):
	"""Given an input file containing float tabular data, returns a list containing
	the x column, and a list of y columns.
	Pound signs may be used as comments; blank lines are skipped.
	For example, if the input file is

	1 2 3
	4 5 6 # Comment here

	7 8 9

	then this routine returns
	[ [1.0, 4.0, 7.0], [[2.0, 5.0, 8.0], [3.0, 6.0, 9.0]] ]
	"""

	columns = float_columns_from_file(file_name)
	return [columns[0], columns[1:]]

# ----------------------------------------------------------------
def xye_columns_from_file(file_name):
	"""Given an input file containing float tabular data, returns a list containing
	the x column, a list of y columns, and a list of error-bar columns.
	Pound signs may be used as comments; blank lines are skipped.
	For example, if the input file is

	1 2 0.2 3 0.3
	4 5 0.2 6 0.3 # Comment here

	7 8 0.2 9 0.3

	then this routine returns
	[
	[1.0, 4.0, 7.0],
	[[2.0, 5.0, 8.0], [3.0, 6.0, 9.0]],
	[[0.2, 0.2, 0.2], [0.3, 0.3, 0.3]]
	]
	"""

	columns = float_columns_from_file(file_name)
	x_columns = columns[0]
	y_columns = []
	e_columns = []
	temp = columns[1:]
	if (len(temp) % 2) != 0:
		print >> sys.stderr, \
		'xye_columns_from_file:  need odd number of columns in file \'%s\'.' \
			% (file_name)
		sys.exit(1)
	num_columns = int(round(len(temp) / 2))
	for j in range(0, num_columns):
		y_columns.append(temp[2*j])
		e_columns.append(temp[2*j+1])

	return [x_columns, y_columns, e_columns]

# ----------------------------------------------------------------
def xye_columns_to_file(x_column, y_columns, e_columns, file_name, \
format='%11.7f'):

	all_columns = [x_column]
	num_series = len(y_columns)
	for j in range(0, num_series):
		all_columns.append(y_columns[j])
		all_columns.append(e_columns[j])
	float_columns_to_file(all_columns, file_name, format)

# ----------------------------------------------------------------
# Example:  If the data file is
#
#   #x y1 y2 y3
#   #- -- -- --
#   1  2  3  4
#   2  4  2  7
#   3  6  5  9
#   4  8  1  5
#
# then this routine returns
#
#   ["x", ["y1", "y2", "y3"]].

def labels_from_file(file_name, split_on_comma=False):

	file_handle = open_file_or_die(file_name, 'r')

	line = file_handle.readline()
	if (line == ""):
		print >> sys.stderr, \
			"tabutil_m.labels_from_file:  couldn't read line 1."
		sys.exit(1)

	if (file_name != "-"):
		file_handle.close()

	# Strip leading whitespace
	line = re.sub(r"^\s+", r"", line)

	# Omit the comment character(s).
	line = re.sub(r"^#+", r"", line)

	# Strip trailing carriage return, if any.
	if line[-1] == '\n':
		line = line[0:-1]
	# Strip leading and trailing whitespace.
	line = re.sub(r"^\s+", r"", line)
	line = re.sub(r"\s+$", r"", line)

	# Split on comma or whitespace.
	if split_on_comma:
		labels  = line.split(',')
	else:
		labels  = line.split()
	return labels

# ----------------------------------------------------------------
# E.g. input file was
#   1  5
#   2  7
#   3  6
# so columns are
#   [[1, 2, 3], [5, 7, 6]].
# Then the tuples are
#   [[1, 5], [2, 7], [3, 6]].

def columns_to_tuples(columns):
	num_columns = len(columns)
	num_tuples  = len(columns[0])
	tuples = []
	for i in range(0, num_tuples):
		tuple = []
		for j in range(0, num_columns):
			tuple.append(columns[j][i])
		tuples.append(tuple)
	return tuples

# ----------------------------------------------------------------
def float_rows_from_file(file_name):
	"""Given an input file containing float tabular data, returns a list of rows.
	Pound signs may be used as comments; blank lines are skipped.
	For example, if the input file is

	1 2 3
	4 5 6 # Comment here

	7 8 9

	then this routine returns
	[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
	"""

	return columns_to_tuples(float_columns_from_file(file_name))

# ----------------------------------------------------------------
def float_columns_to_file(columns, file_name, format="%11.7f"):
	"""Given a list of columns, write the data to a table file.
	For example, if the input is

	[[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]

	then the output file contains

	1.0000 2.0000 3.0000
	4.0000 5.0000 6.0000
	7.0000 8.0000 9.0000
	"""

	num_columns = len(columns)
	num_rows    = len(columns[0])
	text_columns = []
	for j in range(0, num_columns):
		text_column = []
		for i in range(0, num_rows):
			entry = columns[j][i]
			if entry == None:
				text_column.append('_')
			else:
				text_column.append(format % entry)
		text_columns.append(text_column)

	text_columns_to_file(text_columns, file_name)

# ----------------------------------------------------------------
def float_rows_to_file(rows, file_name, format="%11.7f"):
	"""Given a list of rows, write the data to a table file.
	For example, if the input is

	[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

	then the output file contains

	1.0000 2.0000 3.0000
	4.0000 5.0000 6.0000
	7.0000 8.0000 9.0000

	"""

	float_rows_and_labels_to_file(rows, None, file_name, format)

# ----------------------------------------------------------------
def float_rows_and_labels_to_file(rows, labels, file_name, format="%11.7f"):
	"""Given a list of rows, write the data to a table file.
	For example, if the input is

	[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

	and the labels are

	['x', 'y', 'z'],

	then the output file contains

	#x     y      z
	#-     -      -
	1.0000 2.0000 3.0000
	4.0000 5.0000 6.0000
	7.0000 8.0000 9.0000

	"""

	num_rows     = len(rows)
	num_columns  = len(rows[0])
	text_rows = []
	for i in range(0, num_rows):
		text_row = []
		for j in range(0, num_columns):
			entry = rows[i][j]
			if entry == None:
				text_row.append('_')
			else:
				text_row.append(format % entry)
		text_rows.append(text_row)

	text_rows_and_labels_to_file(text_rows, labels, file_name)

# ----------------------------------------------------------------
def print_float_columns(columns, format="%11.7f"):
	float_columns_to_file(columns, '-', format)

# ----------------------------------------------------------------
def float_columns_and_labels_to_file(columns, labels, file_name, \
format="%11.7f"):
	"""Given a list of columns, write the data to a table file.
	For example, if the columns input is

	[[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]

	and the labels input is

	['x', 'y1', 'y2'],

	then the output file contains

	#x     y1     y2
	#-     --     --
	1.0000 2.0000 3.0000
	4.0000 5.0000 6.0000
	7.0000 8.0000 9.0000
	"""

	num_columns = len(columns)
	num_rows    = len(columns[0])
	text_columns = []
	for j in range(0, num_columns):
		text_column = []
		for i in range(0, num_rows):
			entry = columns[j][i]
			if entry == None:
				text_column.append('_')
			else:
				text_column.append(format % entry)
		text_columns.append(text_column)

	text_columns_and_labels_to_file(text_columns, labels, file_name)

# ----------------------------------------------------------------
# Print the data with left alignment.  E.g. if columns =
# [['a', 'bcdef', 'ghi'], ['1234', '56', '789']], then this prints
#
# a     1234
# bcdef 56  
# ghi   789 

def text_columns_to_file(columns, file_name):
	text_columns_and_labels_to_file(columns, None, file_name)

# ----------------------------------------------------------------
# Print the data with left alignment.  E.g. if labels = ['name', 'number'] and
# columns = [['a', 'bcdef', 'ghi'], ['1234', '56', '789']], then this prints
#
# #name  number
# #----  ------
# a      1234
# bcdef  56  
# ghi    789 

def text_columns_and_labels_to_file(columns, labels, file_name):
	num_columns = len(columns)
	num_rows    = len(columns[0])

	# Find width of the longest entry or label in each column.
	max_widths = [0] * num_columns
	for j in range(0, num_columns):
		column = columns[j]
		max_width = 0
		for entry in column:
			width = len(entry)
			if width > max_width:
				max_width = width
		if labels != None:
			width = len(labels[j])
		if j == 0:
			width += 1 # For the preceding # on the label line.
		if width > max_width:
			max_width = width
		max_widths[j] = max_width

	# Print the data with left alignment.
	file_handle = open_file_or_die(file_name, 'w')

	if labels != None:
		# Column labels
		for j in range(0, num_columns):
			if j == 0:
				file_handle.write('#%-*s' % (max_widths[j]-1, labels[j]))
			else:
				file_handle.write(' %-*s' % (max_widths[j], labels[j]))
		file_handle.write('\n')

		# Dash lines
		for j in range(0, num_columns):
			if j == 0:
				file_handle.write('#')
				dashes = '-' * (max_widths[j] - 1)
				file_handle.write(dashes)
			else:
				file_handle.write(' ')
				dashes = '-' * (max_widths[j])
				file_handle.write(dashes)
		file_handle.write('\n')

	# Data
	for i in range(0, num_rows):
		for j in range(0, num_columns):
			if j > 0:
				file_handle.write(' ')
			file_handle.write('%-*s' % (max_widths[j], columns[j][i]))
		file_handle.write('\n')
	if file_name != '-':
		file_handle.close()

# ----------------------------------------------------------------
# Print the data with left alignment.  E.g. if
# rows = [['a', '1234'], ['bcdef', '56'], ['ghi', '789']], then this prints
#
# a     1234
# bcdef 56
# ghi   789

# ----------------------------------------------------------------
def text_rows_to_file(rows, file_name):
	text_rows_and_labels_to_file(rows, None, file_name)

# ----------------------------------------------------------------
# Print the data with left alignment.  E.g. if labels = ['name', 'number'] and
# rows = [['a', '1234'], ['bcdef', '56'], ['ghi', '789']], then this prints
#
# #name number
# #---- ------
# a     1234
# bcdef 56
# ghi   789

def text_rows_and_labels_to_file(rows, labels, file_name):
	num_rows    = len(rows)
	num_columns = len(rows[0])

	# Find width of the longest entry or label in each column.
	max_widths = [0] * num_columns
	for j in range(0, num_columns):
		max_width = 0
		for i in range(0, num_rows):
			entry = rows[i][j]
			width = len(entry)
			if width > max_width:
				max_width = width

		if labels != None:
			width = len(labels[j])
			if j == 0:
				width += 1 # For the preceding # on the label line.
			if width > max_width:
				max_width = width

		max_widths[j] = max_width

	# Print the data with left alignment.
	file_handle = open_file_or_die(file_name, 'w')

	if labels != None:
		# Column labels
		for j in range(0, num_columns):
			if j == 0:
				file_handle.write('#%-*s' % (max_widths[j]-1, labels[j]))
			else:
				file_handle.write(' %-*s' % (max_widths[j], labels[j]))
		file_handle.write('\n')

		# Dash lines
		for j in range(0, num_columns):
			if j == 0:
				file_handle.write('#')
				dashes = '-' * (max_widths[j] - 1)
				file_handle.write(dashes)
			else:
				file_handle.write(' ')
				dashes = '-' * (max_widths[j])
				file_handle.write(dashes)
		file_handle.write('\n')

	# Data
	for i in range(0, num_rows):
		for j in range(0, num_columns):
			if j > 0:
				file_handle.write(' ')
			file_handle.write('%-*s' % (max_widths[j], rows[i][j]))
		file_handle.write('\n')
	if file_name != '-':
		file_handle.close()

# ----------------------------------------------------------------
# Example:  if
#
#   Ls     = ['30', '40', '50']
#   alphas = ['0.001', '0.002']
#   table = [['6.730', '6.740', '6.750'], ['6.830', '6.840', '6.850']]
#
# i.e.
#
#   #L alpha=0.001 alpha=0.002
#   #- ----------- -----------
#   30 6.730       6.830
#   40 6.740       6.840
#   50 6.750       6.850
#
# then
#
#   hash = tabutil_m.table_to_hash(Ls, alphas, table)
#   for L in Ls:
#     for alpha in alphas:
#       print  hash[L][alpha],
#     print
#
# prints
#
#   6.730 6.830
#   6.740 6.840
#   6.750 6.850

def table_to_hash(left_labels, top_labels, columns):
	hash = {}
	for i in range(0, len(left_labels)):
		left_label = left_labels[i]
		hash[left_label] = {}
		for j in range(0, len(top_labels)):
			top_label = top_labels[j]
			hash[left_label][top_label] = columns[j][i]

	return hash

# ----------------------------------------------------------------
def text_array_to_float_array(text_array):
	float_array = []
	for entry in text_array:
		float_array.append(float(entry))
	return float_array

# ----------------------------------------------------------------
# Example:
#
# * matrix = [[1,2,3],[4,5,6]]
# * row_index_name = 'x'
# * row_index_values = [10, 20]
# * col_index_name = 'y'
# * col_index_values = [55, 66, 77]
#
# If transpose == False, output is as follows:
#
#   #x y=55 y=66 y=77
#   #- ---- ---- ----
#   10    1    2    3
#   20    4    5    6
#
# If transpose == True, output is as follows:
#
#   #y x=10 x=20
#   #- ---- ----
#   55    1    4
#   66    2    5
#   77    3    6

def matrix_and_labels_to_file(matrix,
	row_index_name, row_index_values, col_index_name, col_index_values,
	file_name, transpose=False,
	matrix_format='%11.7f', label_format='%.7f'):

	if transpose == False:
		# rows
		long_rows = []
		num_rows = len(matrix)
		for i in range(0, num_rows):
			short_row = matrix[i]
			long_row = [row_index_values[i]] + short_row
			long_rows.append(long_row)

		# labels
		labels = [row_index_name]
		for col_index_value in col_index_values:
			col_index_string = label_format % col_index_value
			labels.append('%s=%s' % (col_index_name, col_index_string))

		float_rows_and_labels_to_file(long_rows, labels, file_name,
			matrix_format)

	else:
		# columns
		augmented_columns = [col_index_values] + matrix

		# labels
		labels = [col_index_name]
		for row_index_value in row_index_values:
			row_index_string = label_format % row_index_value
			labels.append('%s=%s' % (row_index_name, row_index_string))

		float_columns_and_labels_to_file(augmented_columns, labels, file_name,
			matrix_format)
