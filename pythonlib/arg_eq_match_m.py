#!/usr/bin/python -Wall

# ================================================================
# This is a utility module for helping to parse command-line arguments of
# the form "N=10", "eps=1e-6", etc.
#
# John Kerl
# kerl.john.r@gmail.com
# 2009-09-16
# ================================================================

import sys
import re

# ----------------------------------------------------------------
# If there is a match, returns [True, {value}].  Else, returns [False, 0].
# E.g. if called with name_eq_value_pair "N=10", name = "N", and value_scanner
# = int, returns [True, 10].

# xxx fix cmt to match reality

def arg_eq_match(name_eq_value_pair, name, value_scanner, value_list):
	name_eq = name + '='
	len_of_name_eq = len(name_eq)
	regexp = '^' + name_eq
	if re.match(regexp, name_eq_value_pair):
		value_string = name_eq_value_pair[len_of_name_eq:]
		try:
			value = value_scanner(value_string)
		except:
			print >> sys.stderr, 'Couldn\'t parse RHS of \'%s\' as %s.' \
				% (name_eq_value_pair, value_scanner.__name__)
			return False
		value_list[0] = value
		return True
	else:
		return False
