These are source programs in C and Go which compile to efficient binaries for
doing things in my `scripts/fundam` directory (i.e. `..` from here), but more
performantly.

Please see the top of each source file for its build instructions.

Example timing info:

First, build the Go and C implementations:
```
$ go build uniqm.go
$ mv uniqm uniqmgo

$ gcc -std=c99 -O3 -I $mlc \
  $mlc/lib/mlr_globals.c $mlc/lib/mlrutil.c $mlc/containers/hss.c ./uniqm.c \
  -o uniqm
```

The `uniqm.c` uses Miller (http://github.com/johnkerl/miller) as an API, with
```
export mlc=/path/to/git/clone/of/miller/c
```

Then compare throughputs (`in.dat` is a few hundred megabytes of integers, one per line):
```
$ time ../uniqm  < in.dat > out1.dat
real  0m39.582s
user  0m36.970s
sys 0m2.543s

$ time ./uniqmgo  < in.dat > out2.dat
real  0m25.971s
user  0m23.761s
sys 0m2.802s

$ time ./uniqm  < in.dat > out3.dat
real  0m16.207s
user  0m15.799s
sys 0m0.352s
```

Check outputs are the same:
```
$ csum y1 y2 y3
0x6299aaa6  18668886  y1
0x6299aaa6  18668886  y2
0x6299aaa6  18668886  y3
```
