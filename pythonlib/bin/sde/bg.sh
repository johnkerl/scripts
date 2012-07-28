#!/bin/sh

nX=30
nt=500
#test_brownian.py bbbm plot nX=$nX nt=$nt > brownian_test_plot.txt

pgr \
	-l -ms 1 \
	-formats ' - - - - - o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o'  \
	-colors 'grey' \
	-xlabel '$t$' -ylabel '$X_t$' \
	-width 9 -height 7 \
	-o bg.png \
	brownian_test_plot.txt
