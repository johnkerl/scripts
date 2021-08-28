#!/bin/bash

# Builds Go executables

set -xeuo pipefail

for x in hex lensort stamplines uniqm; do
  rm $x
done
