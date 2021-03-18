Files here are general-purpose Linux productivity tools accumulated from my time in the software vocation/avocation.  They are released under the terms of the BSD two-clause license (see [LICENSE.txt](../LICENSE.txt)).

The `fundam` directory contains filters I use each and every day in my work as a software developer.  Many of them are intended to be used as editor filters, e.g. one may left-align a paragraph of text columns by using `!}left` in `vim`.

The `fundam/accel` directory contains optional C/Go implementations of a few of the `fundam` scripts (the latter being Python/Ruby/Perl). These programs take the same inputs and produce the same outputs as their scripted versions, but are faster and thus are more pleasant to use for gigascale file sizes.  Using these I can put `scripts/fundam/accel` in my `$PATH` ahead of `scripts/fundam` and then any accelerators (if they exist) will get picked up automatically.

----------------------------------------------------------------

John Kerl 2012-07-19 
