#!/bin/bash

# Fixes up things I type. Fixes up things LLMs type.

sed -i .emd \
  -e 's/—/---/' \
  -e 's/—/---/' \
  -e 's/^-- /---/' \
  -e 's/ --$/---/' \
  -e 's/ -- /---/g' \
  -e 's/ ---/---/g' \
  -e 's/--- /---/g' \
  -e 's/[ 	][ 	]*$//' \
"$@"
