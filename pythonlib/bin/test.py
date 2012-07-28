#!/usr/bin/python -Wall

import tabutil_m

matrix = [[1,2,3],[4,5,6]]
row_index_name = 'x'
row_index_values = [10, 20]
col_index_name = 'y'
col_index_values = [55, 66, 77]

for transpose in [False, True]:
	tabutil_m.matrix_and_labels_to_file(matrix,
		row_index_name, row_index_values, col_index_name, col_index_values,
		'-', transpose, matrix_format='%d', label_format='%d')
	print

