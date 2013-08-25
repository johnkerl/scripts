#!/usr/bin/python -Wall

from __future__ import division # 1/2 = 0.5, not 0.
import math
from cmath import *
import kerlutil

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2007-07-18
#
# Some routines for visualizing complex maps (e.g. conformals including LFTs).
# Output is meant to be piped to my xgr -lines.
# ================================================================

# ----------------------------------------------------------------
def xy2uv(f, x, y):
	z = x + 1j*y
	w = f(z)
	return [w.real, w.imag]

# ----------------------------------------------------------------
# y2 +---+
#    |   |
# y1 +---+
#    x1  x2

def plot_rect_images(f,  xlo, dx, xhi,  ylo, dy, yhi,  do_horiz=1, do_vert=1, do_input=0, do_output=1):
	xs = kerlutil.mfrange(xlo,dx,xhi)
	ys = kerlutil.mfrange(ylo,dy,yhi)

	for rep in [0, 1]:

		for x in xs:
			x1 = x
			x2 = x+dx
			for y in ys:
				y1 = y
				y2 = y+dy

				if (do_input and (rep == 0)):
					print x1, y1, x2, y1
					print x1, y1, x1, y2
				elif (do_output and (rep == 1)):
					[u11, v11] = xy2uv(f, x1, y1)
					[u12, v12] = xy2uv(f, x1, y2)
					[u21, v21] = xy2uv(f, x2, y1)
					[u22, v22] = xy2uv(f, x2, y2)
					print u11, v11, u12, v12
					print u11, v11, u21, v21

# ----------------------------------------------------------------
def rt2z(r, t, center):
	return r*math.cos(t) + 1j*r*math.sin(t) + center

# ----------------------------------------------------------------
def rt2xy(r, t, center):
	return [r*math.cos(t) + center.real, r*math.sin(t) + center.imag]

# ----------------------------------------------------------------
def plot_circ_images(f,  rlo, dr, rhi,  tlo, dt, thi,  center=0+0j, do_horiz=1, do_vert=1, do_input=0, do_output=1):
	rs = kerlutil.mfrange(rlo,dr,rhi)
	ts = kerlutil.mfrange(tlo,dt,thi)

	for rep in [0, 1]:

		for r in rs:
			r1 = r
			r2 = r+dr
			for t in ts:
				t1 = t
				t2 = t+dt

				[x11, y11] = rt2xy(r1, t1, center)
				[x12, y12] = rt2xy(r1, t2, center)
				[x21, y21] = rt2xy(r2, t1, center)
				[x22, y22] = rt2xy(r2, t2, center)

				if (do_input and (rep == 0)):
					print x11, y11, x21, y21
					print x11, y11, x12, y12
				elif (do_output and (rep == 1)):
					[u11, v11] = xy2uv(f, x11, y11)
					[u12, v12] = xy2uv(f, x12, y12)
					[u21, v21] = xy2uv(f, x21, y21)
					[u22, v22] = xy2uv(f, x22, y22)
					print u11, v11, u12, v12
					print u11, v11, u21, v21

# ----------------------------------------------------------------
def recip(z):
	return 1/z

# ----------------------------------------------------------------
def z1z(z):
	return z+1/z

# ----------------------------------------------------------------
def zn1zp1(z):
	return (z-1)/(z+1)

def zn1zp12(z):
	return zn1zp1(zn1zp1(z))
def zn1zp13(z):
	return zn1zp12(zn1zp1(z))
def zn1zp14(z):
	return zn1zp13(zn1zp1(z))

# ----------------------------------------------------------------
def znizpi(z):
	return (z-1j)/(z+1j)

# ----------------------------------------------------------------
def sinmi(z):
	return sin(-1j*z)

# ----------------------------------------------------------------
# Not a complex function.  Just on R^2.
def F02_4(z):
	x = z.real
	y = z.imag
	u = 2*x - y**2
	v = 2*x*y + sqrt(1-x**2-y**2)
	return u + 1j*v

# ----------------------------------------------------------------
def id(z):
	return z

# ================================================================
# Uncomment one of the following.


# ----------------------------------------------------------------
# exp(z) for z in horizontal strip
#   -4 < x < 4
#    0 < x < pi
#plot_rect_images(exp,  -4, .05, 4,  0, .05, pi,  do_horiz=1, do_vert=1)

# exp(z) for z in horizontal strip
#   -4 < x < 4
#   pi < x < 2pi
#plot_rect_images(exp,  -4, .05, 4,  pi, .05, 2*pi,  do_horiz=1, do_vert=1)

# ----------------------------------------------------------------
# sin(z) for z in rectangle
#   -pi/2 < x < pi/2
#      -2 < y <    2
#plot_rect_images(sin,  -pi/2, .05, pi/2,  -2, .05, 2,  do_horiz=1, do_vert=1)
#plot_rect_images(sin,  -pi/2, .05,  0,    -2, .05, 2,  do_horiz=1, do_vert=1)
#plot_rect_images(sin,   0,    .05, pi/2,  -2, .05, 2,  do_horiz=1, do_vert=1)

# ----------------------------------------------------------------
# cos(z) for z in rectangle
#   -pi/2 < x < pi/2
#      -2 < y <    2
#plot_rect_images(cos,    0,   .05, pi,    -2, .05, 2,  do_horiz=1, do_vert=1)
#plot_rect_images(cos,    0,   .05, pi/2,  -2, .05, 2,  do_horiz=1, do_vert=1)
#plot_rect_images(cos, pi/2,   .05, pi,  -2, .05, 2,  do_horiz=1, do_vert=1)

# ----------------------------------------------------------------
# 1/z for box about origin, avoiding origin
#plot_rect_images(recip,   1, .05, 2,   1, .05, 2)
#plot_rect_images(recip,   1, .05, 2,  -2, .05,-1)
#plot_rect_images(recip,  -2, .05,-1,   1, .05, 2)
#plot_rect_images(recip,  -2, .05,-1,  -2, .05,-1)

# 1/z for box about origin, avoiding origin
#plot_rect_images(recip, .20, .05,    2, .20, .05,    2, do_input=1,do_output=0)
#plot_rect_images(recip, .20, .05,    2,  -2, .05, -.20, do_input=1,do_output=0)
#plot_rect_images(recip,  -2, .05, -.20, .20, .05,    2, do_input=1,do_output=0)
#plot_rect_images(recip,  -2, .05, -.20,  -2, .05, -.20, do_input=1,do_output=0)

#plot_rect_images(recip, .20, .05,    2, .20, .05,    2, do_input=0,do_output=1)
#plot_rect_images(recip, .20, .05,    2,  -2, .05, -.20, do_input=0,do_output=1)
#plot_rect_images(recip,  -2, .05, -.20, .20, .05,    2, do_input=0,do_output=1)
#plot_rect_images(recip,  -2, .05, -.20,  -2, .05, -.20, do_input=0,do_output=1)


# 1/z for horizontal strip right above origin
#plot_rect_images(recip,  -2, .05, 2,  0.05, .05, 1)

# 1/z for next horizontal strip above origin
#plot_rect_images(recip,  -2, .05, 2,  1, .05, 2)

# 1/z for horizontal strip right below origin
#plot_rect_images(recip,  -2, .05, 2,  -0.05, -.05, -1)

# 1/z for next horizontal strip below origin
#plot_rect_images(recip,  -2, .05, 2,  -1, -.05, -2)


# 1/z for vertical strip right of origin
#plot_rect_images(recip, 0.05, .05, 1, -2, .05, 2)

# 1/z for next vertical strip right of origin
#plot_rect_images(recip, 1.0, .05, 2, -2, .05, 2)

# 1/z for half-plane right of x=1
#plot_rect_images(recip, 1.0, .05, 6, -2, .05, 2)

# 1/z for half-plane right of x=2
#plot_rect_images(recip, 2.0, .05, 6, -4, .05, 4, do_input=1, do_output=1)

# 1/z for half-plane right of x=1/2
#plot_rect_images(recip, 0.5, .05, 6, -4, .05, 4, do_input=1, do_output=1)


# 1/z for circle right of origin
#plot_circ_images(recip,  .05, .05, .95,  0, .05, 2*pi, 1+0j, do_input=1, do_output=0)
#plot_circ_images(recip,  .05, .05, .95,  0, .05, 2*pi, 1+0j)

# z + 1/z for box about origin, avoiding origin
#plot_rect_images(z1z,   1, .05, 2,   1, .05, 2)
#plot_rect_images(z1z,   1, .05, 2,  -2, .05,-1)
#plot_rect_images(z1z,  -2, .05,-1,   1, .05, 2)
#plot_rect_images(z1z,  -2, .05,-1,  -2, .05,-1)

# ----------------------------------------------------------------
# z + 1/z for disk about origin, avoiding origin
#plot_circ_images(z1z,  .05, .05, .95,  0, .05, 2*pi, 0+0j, do_input=1, do_output=1)

# z + 1/z for half-disk above origin, avoiding origin
#plot_circ_images(z1z, .05,  .05,  .95,  0, .05, pi, 0j, do_input=1,do_output=1)
#plot_circ_images(z1z, 1.05, .05,  1.95, 0, .05, pi, 0j, do_input=1,do_output=1)
#plot_circ_images(z1z, 0.05, .05,  1.95, 0, .05, pi, 0j, do_input=1,do_output=1)
#plot_circ_images(z1z, 0.95, .005, 1.05, 0, .05, pi, 0j, do_input=1,do_output=1)

# z + 1/z for half-disk below origin, avoiding origin
#plot_circ_images(z1z,  .05, .05, .95,  pi, .05, 2*pi, 0+0j, do_input=1, do_output=1)

# ----------------------------------------------------------------
# (z-1)/(z+1) for circle right of origin
#plot_circ_images(zn1zp1,  .05, .05, .95,  0, .05, 2*pi, 1+0j)

# (z-1)/(z+1) box about origin, avoiding origin
#plot_rect_images(zn1zp1,   1, .05, 2,   1, .05, 2)
#plot_rect_images(zn1zp1,   1, .05, 2,  -2, .05,-1)
#plot_rect_images(zn1zp1,  -2, .05,-1,   1, .05, 2)
#plot_rect_images(zn1zp1,  -2, .05,-1,  -2, .05,-1)

# (z-1)/(z+1) for right half-plane
#plot_rect_images(zn1zp1,  0, .05, 4,  -4, .05, 4, do_input=1, do_output=1)

# (z-1)/(z+1) for disk about origin, avoiding origin
#plot_circ_images(zn1zp1,  .05, .05, .95,  0, .05, 2*pi, 0+0j, do_input=1, do_output=1)

# (z-1)/(z+1) for right half-plane
#plot_rect_images(zn1zp1,   -6, .05, -.05,   -6, .05, 6)

# Iterate (z-1)/(z+1) for disk about origin, avoiding origin
#plot_circ_images(zn1zp1,  .05, .05, .95, 0, .05, 2*pi, 0j,do_input=1,do_output=1)
#plot_circ_images(zn1zp12, .05, .05, .95, 0, .05, 2*pi, 0j,do_input=1,do_output=1)
#plot_circ_images(zn1zp13, .05, .05, .95, 0, .05, 2*pi, 0j,do_input=1,do_output=1)
#plot_circ_images(zn1zp14, .05, .05, .95, 0, .05, 2*pi, 0j,do_input=1,do_output=1)

# (z-1)/(z+1) for semi-infinite strip
#plot_rect_images(zn1zp1,   0, .05, 1,   0, .05, 9)
#plot_rect_images(zn1zp1,   0, .05, 9,   0, .05, 1)

# ----------------------------------------------------------------
# (z-i)/(z+i) box about origin, avoiding origin
#plot_rect_images(znizpi,   1, .05, 2,   1, .05, 2)
#plot_rect_images(znizpi,   1, .05, 2,  -2, .05,-1)
#plot_rect_images(znizpi,  -2, .05,-1,   1, .05, 2)
#plot_rect_images(znizpi,  -2, .05,-1,  -2, .05,-1)

# (z-i)/(z+i) for disk about origin, avoiding origin
#plot_circ_images(znizpi,  .05, .05, .95,  0, .05, 2*pi, 0+0j, do_input=1, do_output=1)

# ================================================================

# sin(z), semi-infinite strip  0<x<1 and 0<y
#plot_rect_images(sin,   0, .05, 1,   0, .05, 4)

# sin(z), semi-infinite strip  x<0 and 0<y<1
#plot_rect_images(sin,   -2*pi, .05, 0,   0, .05, 1)

# sin(-iz), semi-infinite strip  0<x<1 and 0<y
#plot_rect_images(sinmi,   0, .05, 1,   0, .05, 2*pi)

# ================================================================
#plot_rect_images(F02_4, -1, .05, 1, -1, .05, 1)
#plot_rect_images(F02_4, .5, .05, 1.5, .5, .05, 1.5)
plot_rect_images(F02_4, -.1, .005, .1, -.1, .005, .1)
