#!/usr/bin/env python

import sys

def cmp(name_and_typename):
    """
   Sorts primarily lexically by typename, then secondarily lexically by name.
    """
    return name_and_typename[1] + ":" + name_and_typename[0]

def describe_module_components(module, include_dunders):
    names_and_typenames = []
    for name in sorted(dir(module)):
        if include_dunders or not name.startswith("__"):
            typename = type(module.__getattribute__(name)).__qualname__
            names_and_typenames.append((name, typename))
    names_and_typenames = sorted(names_and_typenames, key=cmp)
    for name, typename in names_and_typenames:
        print("%-30s %s" % (name, typename))

if __name__ == "__main__":
    include_dunders = False
    names = sys.argv[1:]
    if len(names) >= 1 and names[0] == "-a":
        include_dunders = True
        names = names[1:]
    for name in names:
        module = __import__(name, fromlist=[""])
        describe_module_components(module, include_dunders)
