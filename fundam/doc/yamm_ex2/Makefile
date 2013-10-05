# ================================================================
# Makefile for project cmdsample
# Automatically generated from "cmdsample.mki" at Thu Feb 11 09:58:42 2010

# yamm v1.0
# John Kerl
# 2002/05/04
# ================================================================


INCLUDE_DIRS = -I.
LIB_DIRS =
DEFINES = -DUNIX -DHOSTED -DNO_BOOL -Dterm_printf=printf -Dut_memset=memset -Dut_memcpy=memcpy -Dut_strlen=strlen -Dut_strcpy=strcpy -Dut_strcat=strcat -Dut_strcmp=strcmp -Dut_sprintf=sprintf
MISC_CFLAGS =
MISC_LFLAGS =
EXTRA_DEPS =
COMPILE_FLAGS = -c $(INCLUDE_DIRS) $(DEFINES) $(MISC_CFLAGS)
LINK_FLAGS =  $(LIB_DIRS) $(MISC_LFLAGS)

build: mk_obj_dir ./cmdsample

mk_obj_dir:
	mkdir -p objs

objs/cmdsample.o:  ./cmdfactor.h ./cmdgcd.h ./tokenize.h cmdsample.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  cmdsample.c -o objs/cmdsample.o

objs/cmdfactor.o:  ./cmdfactor.h ./factor.h cmdfactor.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  cmdfactor.c -o objs/cmdfactor.o

objs/cmdgcd.o:  ./cmdgcd.h ./gcd.h cmdgcd.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  cmdgcd.c -o objs/cmdgcd.o

objs/factor.o:  ./factor.h factor.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  factor.c -o objs/factor.o

objs/gcd.o:  ./gcd.h gcd.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  gcd.c -o objs/gcd.o

objs/hcmd.o:  ./hcmd.h hcmd.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  hcmd.c -o objs/hcmd.o

objs/tokenize.o:  ./tokenize.h tokenize.c
	gcc -Wall -Werror -g $(COMPILE_FLAGS)  tokenize.c -o objs/tokenize.o

OBJS = \
	objs/cmdsample.o \
	objs/cmdfactor.o \
	objs/cmdgcd.o \
	objs/factor.o \
	objs/gcd.o \
	objs/hcmd.o \
	objs/tokenize.o

./cmdsample: $(OBJS) $(EXTRA_DEPS)
	gcc $(OBJS) -o ./cmdsample $(LINK_FLAGS)

clean:
	-@rm -f $(OBJS)
	-@rm -f ./cmdsample
