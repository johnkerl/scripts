#!/bin/bash

for x in $(find . -name '*.qmd' -o -name '*.md'); do
    sed -i .emd \
      -e 's/—/---/g' \
      -e 's/—/---/g' \
      -e 's/^-- /---/g' \
      -e 's/ --$/---/g' \
      -e 's/ -- /---/g' \
      -e 's/ ---/---/g' \
      -e 's/--- /---/g' \
      -e 's/[ 	][ 	]*$//g' \
    $x
    rm $x.emd
done
