# ================================================================
# Makefile for project sample
# Automatically generated from "sample.mki" at Thu Feb 11 09:53:17 2010

# yamm v1.0
# John Kerl
# 2002/05/04
# ================================================================


INCLUDE_DIRS =
LIB_DIRS =
DEFINES =
MISC_CFLAGS =
MISC_LFLAGS =
EXTRA_DEPS =
COMPILE_FLAGS = -c $(INCLUDE_DIRS) $(DEFINES) $(MISC_CFLAGS)
LINK_FLAGS =  $(LIB_DIRS) $(MISC_LFLAGS)

build: mk_obj_dir ./sample

mk_obj_dir:
	mkdir -p ./sample_objs

./sample_objs/file1.o:  file1.c myheader.h
	gcc $(COMPILE_FLAGS)  file1.c -o ./sample_objs/file1.o

./sample_objs/file2.o:  file2.c myheader.h
	gcc $(COMPILE_FLAGS)  file2.c -o ./sample_objs/file2.o

OBJS = \
	./sample_objs/file1.o \
	./sample_objs/file2.o

./sample: $(OBJS) $(EXTRA_DEPS)
	gcc $(OBJS) -o ./sample $(LINK_FLAGS)

clean:
	-@rm -f $(OBJS)
	-@rm -f ./sample
