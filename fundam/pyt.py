#!/usr/bin/env python

# ================================================================
# See ./pyt for context
# ================================================================

import os, sys, getopt, random, time, math

import tiledb

import numpy   as np
import pandas  as pd
import pyarrow as pa
import anndata as ad

print('tiledb.version()         ', tiledb.version(), tiledb.__file__)
print('core version             ', ".".join(str(ijk) for ijk in list(tiledb.libtiledb.version())), tiledb.libtiledb.__file__)
print('numpy.__version__    (np)', np.__version__)
print('pandas.__version__   (pd)', pd.__version__)
print('pyarrow.__version__  (pa)', pa.__version__)
print('python__version__        ', ".".join([str(e) for e in [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]]))

# ----------------------------------------------------------------
import readline
def history(n=10):
    history_length = readline.get_current_history_length()
    history_range = range(history_length - n, history_length)
    lines = [str(readline.get_history_item(i + 1)) for i in history_range]
    print('\n'.join(lines))
# ----------------------------------------------------------------


pass
# Take further stuff from the '>>> ' prompt

