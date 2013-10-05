This is a sample program to illustrate the use of the yamm makefile generator.

Instructions:

* Obtain the source files (.c and .h).

* Obtain the make-input file (.mki)

* Obtain the Perl script yamm.

* Type "yamm sample.mki" at the shell prompt to have yamm read sample.mki
  and generate the makefile sample.mk

* Type "make -f sample.mk" at the shell prompt to build the program, "sample".

* Type "sample" at the shell prompt to run the executable.  It prints
  "Hello, world!".

Notes:  You need to rerun yamm only if you modify the .mki, or if you
add/remove header inclusions in your source files.  If you don't know what
that means, or if you are uncertain, it is quite OK to go ahead and run yamm
before every time you run make.

John Kerl
2003/10/20
