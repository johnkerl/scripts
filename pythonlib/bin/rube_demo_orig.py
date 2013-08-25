#!/usr/bin/python -Wall

# ================================================================
# Copyright (c) John Kerl 2007
# kerl.john.r@gmail.com
# ================================================================

from rube_m import *

tell_about(['F'])
tell_about(['F', 'R'])
tell_about(['F', 'R-'])
tell_about(['F', 'R2'])
tell_about(['F', 'U', 'R'])
tell_about(['F', 'R', 'F', 'R'])
tell_about(['F', 'R', 'B', 'L'])
tell_about(['F', 'R', 'B', 'L', 'D', 'U'])
tell_about(['F', 'U', 'R', 'B', 'D', 'L'])
tell_about(['F', 'U', 'R', 'B', 'L', 'D'])
tell_about(conjugate(['F', 'R'], ['B', 'L']))
tell_about(commutator(['F', 'R'], ['B', 'L']))
tell_about(['F2', 'R2'])
tell_about(['F2'])
tell_about(['F2', 'B2'])
tell_about(conjugate(['B'], power_of_sequence(['L', 'U', 'L-', 'U-'], 3)))
tell_about(power_of_sequence(['B', 'R-', 'D2', 'R', 'B-', 'U2'], 1))
tell_about(power_of_sequence(['B', 'R-', 'D2', 'R', 'B-', 'U2'], 2))

bot_tri_rot = ['L-', 'R+', 'F+', 'L+', 'R-', 'D2', 'L-', 'R+', 'F+', 'L+', 'R-' ]
tell_about(bot_tri_rot)

bot_two_flip = [ \
	'R', 'L-', 'F',  'R-', 'L', 'D',
	'R', 'L-', 'F',  'R-', 'L', 'D',
	'R', 'L-', 'F2', 'R-', 'L', 'D',
	'R', 'L-', 'F',  'R-', 'L', 'D',
	'R', 'L-', 'F',  'R-', 'L', 'D2']
tell_about(bot_two_flip)

tell_about(['B-', 'U2', 'B2', 'U', 'B-', 'U-', 'B-', 'U2', 'F', 'R', 'B', 'R-', 'F-'])

