#!/bin/bash

# Builds Rust executables

set -xeuo pipefail

for x in hex; do
  rustc rsmains/$x/$x.rs
done
