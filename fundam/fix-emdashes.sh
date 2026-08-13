#!/bin/bash

# Fixes up things I type. Fixes up things LLMs type.

flag=""
if [ $# -gt 0 ]; then
  flag="-i .emd"
fi

sed $flag \
  -e 's/—/---/g' \
  -e 's/—/---/g' \
  -e 's/^-- /---/g' \
  -e 's/ --$/---/g' \
  -e 's/ -- /---/g' \
  -e 's/ ---/---/g' \
  -e 's/--- /---/g' \
  -e 's/[ 	][ 	]*$//g' \
"$@"
