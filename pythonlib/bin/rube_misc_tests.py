#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from rube_m import *

# ----------------------------------------------------------------
def rube_test_1():

	print piece_equal('UFR', 'FRU')
	print piece_equal('FUR', 'FUR')
	print piece_equal('FUR', 'FU')
	print

	print move_on_face('U+', 'F')
	print move_on_corner_piece('F', 'URF')
	print move_on_corner_piece('F', 'URL')
	print moves_on_piece(['U', 'F', 'R'], 'UFR')
	print

	print moves_on_piece(['F', 'F', 'F', 'F'], 'UFR')
	print moves_on_piece(['F'], 'UFR')
	print moves_on_piece(['F'], 'UF')
	print

	print moves_on_pieces(['F'],                ['UFR', 'UF'])
	print moves_on_pieces(['F', 'F'],           ['UFR', 'UF'])
	print moves_on_pieces(['F', 'F', 'F'],      ['UFR', 'UF'])
	print moves_on_pieces(['F', 'F', 'F', 'F'], ['UFR', 'UF'])
	print

	print "<<", sign_of_rotation('UFR', 'UFL'), ">>"
	print "<<", sign_of_rotation('UFR', 'UFR'), ">>"
	print "<<", sign_of_rotation('UFR', 'URF'), ">>"
	print "<<", sign_of_rotation('FUR', 'FRU'), ">>"
	print "<<", sign_of_rotation('UFR', 'UR'), ">>"
	print

	print "FIND CYCLE:"
	print find_cycle(['U', 'L'], 'UFR')
	print

	print "FIND CYCLES:"
	print find_cycles(['U'], ['UFR', 'UFL', 'DFR', 'DFL'])
	print find_cycles(['U', 'L'], ['UFR', 'UFL'])
	print find_cycles(['F', 'R', 'B', 'L'], ['UF', 'UL', 'UFR', 'UFL'])
	print

	print "DELETE 1-CYCLES:"
	print delete_1_cycles(find_cycles(['U'], ['UFR', 'UFL', 'DFR', 'DFL']))
	print delete_1_cycles(find_cycles(['U', 'L'], ['UFR', 'UFL']))
	print delete_1_cycles(find_cycles(['F', 'R', 'B', 'L'], ['UF', 'UL', 'UFR', 'UFL']))
	print

	print "CYCLE DECOMPOSITION:"
	print cycle_decomposition(["F"])
	print cycle_decomposition(["F", "R"])
	print cycle_decomposition(["F", "R", "B", "L"])
	print cycle_decomposition(["F2", "R2"])
	print cycle_decomposition(["F2"])
	print cycle_decomposition(["F2", "B2"])
	print

	print "PRINT CYCLE DECOMPOSITION:"
	print_cycle_decomposition(["F"])
	print_cycle_decomposition(["F", "R"])
	print_cycle_decomposition(["F", "R", "B", "L"])
	print_cycle_decomposition(["F2", "R2"])
	print_cycle_decomposition(["F2"])
	print_cycle_decomposition(["F2", "B2"])
	print

	print "IMAGES:"
	print images_of_all_pieces(["F"])
	print images_of_all_pieces(["F", "R"])
	print images_of_all_pieces(["F", "R", "B", "L"])
	print images_of_all_pieces(["F2", "R2"])
	print images_of_all_pieces(["F2"])
	print images_of_all_pieces(["F2", "B2"])
	bot_tri_rot = ["L-", "R+", "F+", "L+", "R-", "D2", "L-", "R+", "F+", "L+", "R-" ]
	print images_of_all_pieces(bot_tri_rot)
	print

	print "ORDERS:"
	print order(["F"])
	print order(["F", "R"])
	print order(["F", "R", "B", "L"])
	print order(["F2", "R2"])
	print order(["F2"])
	print order(["F2", "B2"])
	bot_tri_rot = ["L-", "R+", "F+", "L+", "R-", "D2", "L-", "R+", "F+", "L+", "R-" ]
	print order(bot_tri_rot)
	print

rube_test_1()
