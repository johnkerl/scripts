#!/bin/bash

for x in $(find . -name '*.qmd' -o -name '*.md'); do
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
