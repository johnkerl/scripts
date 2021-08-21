# Builds C executables

all: hex uniqm

hex: hex.c
	gcc -std=c99 hex.c -o hex

uniqm: clib/util.h clib/util.c clib/hss.h clib/hss.c clib/argf.h clib/argf.c uniqm.c
	gcc -std=c99 -O3 -Iclib clib/util.c clib/hss.c clib/argf.c uniqm.c -o uniqm

clean:
	rm -f hex uniqm
