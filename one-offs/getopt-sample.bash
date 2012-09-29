#!/bin/bash

# ================================================================
# A bash-getopt cheat sheet.
# ================================================================

# ----------------------------------------------------------------
usage() {
	echo "Usage: $(basename $0) {-a aarg} {-f farg} {-i iarg} {-l}" 1>&2
	exit 1
}

# ----------------------------------------------------------------
aarg="adefault"
farg=
lopt=0

while getopts a:f:l? f
do
	case $f in
	a)      aarg="$OPTARG"; continue;;
	f)      farg="$OPTARG"; continue;;
	l)      lopt=1;         continue;;
	\?)     echo; usage;;
	esac
done
shift $(($OPTIND-1))
non_option_args="$@"
non_option_arg_count=$#

echo "aarg=$aarg"
echo "farg=$farg"
echo "lopt=$lopt"
echo "# non-option args: $non_option_arg_count"
for arg in $non_option_args; do
	echo "Non-option arg: $arg"
done
