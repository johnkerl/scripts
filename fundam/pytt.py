#!/usr/bin/env python

# ================================================================
# See ./pytt for context
# ================================================================

import os, sys, getopt, random, time, math, json

# ----------------------------------------------------------------
try:
    import tiledbsoma
    print('tiledbsoma.__version__   ', tiledbsoma.__version__, tiledbsoma.__file__)
    soma = tiledbsoma
    t = tiledbsoma
    import tiledbsoma.io
    tio = tiledbsoma.io
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> tiledbsoma module not found")

try:
    import tiledbsoma.io
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> tiledbsoma.io module not found")

# ----------------------------------------------------------------
try:
    import tiledbsoma.pytiledbsoma as clib
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    clib = None

if clib is not None:
    # Example:
    # 'libtiledbsoma=2be3147\nlibtiledb=2.12.2'
    lines = tiledbsoma.pytiledbsoma.version().split("\n")
    if len(lines) == 1:
        print("%-25s %s %s" % ("libtiledbsoma", lines[0], tiledbsoma.pytiledbsoma.__file__))
    else:
        for line in lines:
            name, version = line.split("=")
            path = ""
            if name == "libtiledbsoma":
                path = " " + tiledbsoma.pytiledbsoma.__file__
            print("%-25s %s %s" % (name, version, path))

# ----------------------------------------------------------------
try:
    import somacore
    print('somacore.__version__     ', somacore.__version__, somacore.__file__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> somacore module not found")

# ----------------------------------------------------------------
try:
    import tiledb
    print('tiledb.version           ', ".".join(str(e) for e in tiledb.version()), tiledb.__file__)
    print('core version             ', ".".join(str(ijk) for ijk in list(tiledb.libtiledb.version())), tiledb.libtiledb.__file__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> tiledb module not found")

# ----------------------------------------------------------------
try:
    import anndata as ad
    print('anndata.__version__  (ad)', ad.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> anndata module not found")

try:
    import numpy   as np
    print('numpy.__version__    (np)', np.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> numpy module not found")

try:
    import numba
    print('numba.__version__    (np)', numba.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> numba module not found")

try:
    import pandas  as pd
    print('pandas.__version__   (pd)', pd.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> pandas module not found")

try:
    import pyarrow as pa
    print('pyarrow.__version__  (pa)', pa.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> pyarrow module not found")

try:
    import scanpy  as sc
    print('scanpy.__version__   (sc)', sc.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> scanpy module not found")

try:
    import scipy   as sp
    print('scipy.__version__    (sp)', sp.__version__)
except (ModuleNotFoundError, AttributeError, FileNotFoundError):
    print(">>>>>>>> scipy module not found")

print('python__version__        ', ".".join([str(e) for e in [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]]))

print()
tiledbsoma.show_package_versions()

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
