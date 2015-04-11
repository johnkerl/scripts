#!/usr/bin/env python

# ================================================================
# A python-getopt cheat sheet.
# ================================================================

import os, sys, getopt

# ----------------------------------------------------------------
def usage():
	print >> sys.stderr, "Usage: %s {-a aarg} {-f farg} {-i iarg} {-l}" % os.path.basename(sys.argv[0])
	sys.exit(1)

# ----------------------------------------------------------------
aarg = "adefault"
farg = None
iarg = None
lopt = 0

try:
	optargs, non_option_args = getopt.getopt(sys.argv[1:], "a:f:i:l", ['help'])
except getopt.GetoptError, err:
	print str(err)
	usage()
	sys.exit(1)

for opt, arg in optargs:
    if opt == '-a':
		aarg = arg
    elif opt == '-f':
		farg = float(arg)
    elif opt == '-i':
		iarg = int(arg)
    elif opt == '-l':
		lopt = 1
    elif opt == '--help':
		usage()
    else:
		print >> sys.stderr, "Unhandled option \"%s\"." % opt
		sys.exit(1)

non_option_arg_count = len(non_option_args)

print "aarg = %s" % aarg
print "farg = %s" % farg
print "iarg = %s" % iarg
print "lopt = %s" % lopt
print "# non-option args: %d " % non_option_arg_count
for arg in non_option_args:
	print "Non-option arg: %s" % arg
