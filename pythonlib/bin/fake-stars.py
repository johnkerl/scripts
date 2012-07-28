#!/usr/bin/python -Wall

# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2011-03-06
# Makes a pseudo-starry-sky image suitable for wallpaper.
# ================================================================

from __future__ import division
import sys, Image
import random

# ----------------------------------------------------------------
# Tweakable parameters
density = 0.01
radius_CDF = [[0.9, 1], [0.98, 2], [1.0, 3]]
spread = 40

# ----------------------------------------------------------------
def main():
	# My laptop monitor size:
	#width = 1366
	#height = 768

	# My laptop monitor size times 120%.  Then I can shrink the image
	# inside GIMP to get a little softer look.
	width = 1640
	height = 922

	argc = len(sys.argv)
	if argc == 2:
		file_name = sys.argv[1]
	elif argc == 4:
		width  = int(sys.argv[1])
		height = int(sys.argv[2])
		file_name = sys.argv[3]
	else:
		usage()

	im = Image.new('RGB', (width, height), 0)

	num_stars = int(density * width * height)
	for k in xrange(0, num_stars):
		i = random.randint(0, width-1)
		j = random.randint(0, height-1)
		putrandstar(im, width, height, i, j)

	im.save(file_name)

# ----------------------------------------------------------------
def usage():
	print >> sys.stderr, \
		"Usage: %s {width in pixels} {height in pixels} {output file name}"
	sys.exit(1)

# ----------------------------------------------------------------
# 1. Keep r/g/b close to one another, & vary brightness more.
# 2. Take random radius & bleed over into adjacent pixels

def putrandstar(im, width, height, i, j):
	r = random.randint(0, 255)
	g = random.randint(max(r-spread,0), min(r+spread,255))
	b = random.randint(max(r-spread,0), min(r+spread,255))

	radius = random_selection_from_CDF(radius_CDF)

	# How to handle various radii:  treat the star as a circular disk, with
	# brightness uniform across the disk.  So, for each pixel in a 1x1, 2x2, or
	# 3x3 grid, count the fraction of the pixel that is covered by a circle.
	# (Place star centers at pixel centers for convenience.)

	# Eyeball estimates:
	# o 1x1: middle about 3/4 covered.
	# o 2x2: center 100% covered.  up/down/left/right about 45% covered.
	#        corners about 15% covered.
	# o 3x3: center 100% covered.  up/down/left/right about 90% covered.
	#        corners about 60% covered.

	if radius == 1:
		im.putpixel((i,j), scale_rgb(r,g,b,0.75))
	elif radius == 2:

		clipped_putpixel(im, width, height, i,   j,   scale_rgb(r,g,b,1.00))

		clipped_putpixel(im, width, height, i+1, j,   scale_rgb(r,g,b,0.45))
		clipped_putpixel(im, width, height, i-1, j,   scale_rgb(r,g,b,0.45))
		clipped_putpixel(im, width, height, i,   j+1, scale_rgb(r,g,b,0.45))
		clipped_putpixel(im, width, height, i,   j-1, scale_rgb(r,g,b,0.45))

		clipped_putpixel(im, width, height, i+1, j+1, scale_rgb(r,g,b,0.15))
		clipped_putpixel(im, width, height, i+1, j-1, scale_rgb(r,g,b,0.15))
		clipped_putpixel(im, width, height, i-1, j+1, scale_rgb(r,g,b,0.15))
		clipped_putpixel(im, width, height, i-1, j-1, scale_rgb(r,g,b,0.15))

	elif radius == 3:

		clipped_putpixel(im, width, height, i,   j,   scale_rgb(r,g,b,1.00))

		clipped_putpixel(im, width, height, i+1, j,   scale_rgb(r,g,b,0.90))
		clipped_putpixel(im, width, height, i-1, j,   scale_rgb(r,g,b,0.90))
		clipped_putpixel(im, width, height, i,   j+1, scale_rgb(r,g,b,0.90))
		clipped_putpixel(im, width, height, i,   j-1, scale_rgb(r,g,b,0.90))

		clipped_putpixel(im, width, height, i+1, j+1, scale_rgb(r,g,b,0.40))
		clipped_putpixel(im, width, height, i+1, j-1, scale_rgb(r,g,b,0.40))
		clipped_putpixel(im, width, height, i-1, j+1, scale_rgb(r,g,b,0.40))
		clipped_putpixel(im, width, height, i-1, j-1, scale_rgb(r,g,b,0.40))

# ----------------------------------------------------------------
def random_selection_from_CDF(CDF):
	U = random.uniform(0.0, 1.0)
	for [C, value] in CDF:
		if U < C:
			return value
	print >> sys.stderr, 'random_selection_from_CDF b0rk'
	sys.exit(1)

# ----------------------------------------------------------------
def scale_rgb(r,g,b,frac):
	return (int(frac*r), int(frac*g), int(frac*b))

# ----------------------------------------------------------------
def clipped_putpixel(im, width, height, i, j, rgb):
	if i < 0:
		return
	if i >= width:
		return
	if j < 0:
		return
	if j >= height:
		return
	im.putpixel((i,j), rgb)

# ================================================================
main()
