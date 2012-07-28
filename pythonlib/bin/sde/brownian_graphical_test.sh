#!/bin/sh


nX=30
nt=500
#test_brownian.py bbbm plot nX=$nX nt=$nt > brownian_test_plot.txt

pgr \
	-l \
	-xlabel '$t$' -ylabel '$X_t$' \
	-title $nX' Brownian bridges with $\mu_t$, $\mu_t\pm\sigma_t$, and $\mu_t\pm 2 \sigma_t$'. \
	-width 8 -height 6 \
	-o brownian_test_plot.png \
	brownian_test_plot.txt
