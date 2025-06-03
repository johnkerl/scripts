#!/usr/bin/env python

import sys

unique_lines = set({})
for line in sys.stdin:
    if line not in unique_lines:
        sys.stdout.write(line)
        unique_lines.add(line)
