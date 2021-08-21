#!/bin/bash

# Builds Go executables

set -xeuo pipefail

for x in hex lensort stamplines uniqm; do
  cd gomains/$x
  go build
  mv $x ../..
  cd ../..
done
