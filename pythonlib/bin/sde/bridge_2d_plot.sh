#!/bin/sh

nR=20
nt=2000
X0=-2
Y0=-1
XT=3
YT=4
T=2
test_bridge_2d.py nR=$nR nt=$nt > bridge_2d_plot.txt

pgr \
	-xyxy -l -grey \
	-xlabel '$X_t$' -ylabel '$Y_t$' \
	-title $nR' Brownian bridges from ('$X0','$Y0') to ('$XT','$YT') in time '$T''. \
	-width 8 -height 6 \
	-o bridge_2d_plot.png \
	bridge_2d_plot.txt
