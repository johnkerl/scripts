#!/usr/bin/env python

# ================================================================
# See ./pytt for context
# ================================================================

import os, sys, getopt, random, time, math

# ----------------------------------------------------------------
try:
    import tiledb
    print('tiledb.version           ', ".".join(str(e) for e in tiledb.version()), tiledb.__file__)
    print('core version             ', ".".join(str(ijk) for ijk in list(tiledb.libtiledb.version())), tiledb.libtiledb.__file__)
except ModuleNotFoundError:
    print("tiledb module not found")
    sys.exit(1)

# ----------------------------------------------------------------
try:
    import tiledbsoma
    print('tiledbsoma.__version__   ', tiledbsoma.__version__, tiledbsoma.__file__)
except ModuleNotFoundError:
    print("tiledbsoma module not found")
    sys.exit(1)
soma = tiledbsoma

try:
    import tiledbsoma.io
except ModuleNotFoundError:
    print("tiledbsoma.io module not found")
    sys.exit(1)

# ----------------------------------------------------------------
try:
    import tiledbsoma.libtiledbsoma as clib
except ModuleNotFoundError:
    # main-old
    clib = None
except ImportError:
    # main-old
    clib = None

if clib is not None:
    # Example:
    # 'libtiledbsoma=2be3147\nlibtiledb=2.12.2'
    lines = tiledbsoma.libtiledbsoma.version().split("\n")
    for line in lines:
        name, version = line.split("=")
        path = ""
        if name == "libtiledbsoma":
            path = " " + tiledbsoma.libtiledbsoma.__file__
        print("%-25s %s%s" % (name, version, path))

# ----------------------------------------------------------------
try:
    import somacore
    print('somacore.__version__     ', somacore.__version__, somacore.__file__)
except ModuleNotFoundError:
    print("somacore module not found")
    sys.exit(1)

# ----------------------------------------------------------------
try:
    import anndata as ad
    print('anndata.__version__  (ad)', ad.__version__)
except ModuleNotFoundError:
    print("anndata module not found")
    sys.exit(1)

try:
    import numpy   as np
    print('numpy.__version__    (np)', np.__version__)
except ModuleNotFoundError:
    print("numpy module not found")
    sys.exit(1)

try:
    import numba
    print('numba.__version__    (np)', numba.__version__)
except ModuleNotFoundError:
    print("numba module not found")
    sys.exit(1)

try:
    import pandas  as pd
    print('pandas.__version__   (pd)', pd.__version__)
except ModuleNotFoundError:
    print("pandas module not found")
    sys.exit(1)

try:
    import pyarrow as pa
    print('pyarrow.__version__  (pa)', pa.__version__)
except ModuleNotFoundError:
    print("pyarrow module not found")
    sys.exit(1)

try:
    import scanpy  as sc
    print('scanpy.__version__   (sc)', sc.__version__)
except ModuleNotFoundError:
    print("scanpy module not found")
    sys.exit(1)

try:
    import scipy   as sp
    print('scipy.__version__    (sp)', sp.__version__)
except ModuleNotFoundError:
    print("scipy module not found")
    sys.exit(1)

print('python__version__        ', ".".join([str(e) for e in [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]]))

# ----------------------------------------------------------------
import readline
def history(n=10):
    history_length = readline.get_current_history_length()
    history_range = range(history_length - n, history_length)
    lines = [str(readline.get_history_item(i + 1)) for i in history_range]
    print('\n'.join(lines))
# ----------------------------------------------------------------

#ctx = tiledb.Ctx(
#    {
#        "sm.mem.total_budget": 4 * 1024 ** 3,
#        "sm.consolidation.buffer_size": 512 * 1024 ** 2,
#        # "sm.consolidation.mode": "fragments", # This is the default -- ?
#        # "sm.consolidation.mode": "fragment_meta",
#        "sm.consolidation.mode": "commits",
#        # "sm.consolidation.mode": "array_meta",
#    }
#)

ctx = tiledb.Ctx({
    "py.init_buffer_bytes": 4 * 1024**3,
    # "rest.use_refactored_array_open": True,
    "sm.mem.reader.sparse_global_order.ratio_array_data": 0.3,
})


pass
# Take further stuff from the '>>> ' prompt