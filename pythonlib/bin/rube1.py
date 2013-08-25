#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from rube_m import *
import sys
import re

argc = len(sys.argv)
if (argc < 2):
	print >> sys.stderr, "Usage:   %s [string]" % (sys.argv[0])
	print >> sys.stderr, "Example: %s \"['F2', 'R2'] * 3\"" % (sys.argv[0])
	sys.exit(1)

string = sys.argv[1]
for i in range(2, argc):
	string += ' '
	string += sys.argv[i]
print string
if (re.match('\[', string)):
	tell_about(eval(string))
else:
	tell_about(rube_unpack(string))
#tell_about(string)
