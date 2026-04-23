#!/bin/bash

for x in $(find . -name '*.qmd'); do
    sed -i .emd \
      -e 's/—/---/' \
      -e 's/—/---/' \
      -e 's/^-- /---/' \
      -e 's/ --$/---/' \
      -e 's/ -- /---/g' \
      -e 's/ ---/---/g' \
      -e 's/--- /---/g' \
      -e 's/[ 	][ 	]*$//' \
    $x
    rm $x.emd
done
