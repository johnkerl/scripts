from __future__ import division # 1/2 = 0.5, not 0.
from sackmatc_m import *
import sys

Q = m([[0.28,0.96j],[-0.96j,-0.28]])
v=[.6,.8j]
Qv = Q*v
print "Q= " ; Q.printf(); print
print "v= ",; print_column_vector(v); print
print "Qv=",; print_column_vector(Qv); print
print

Q = m([[0.28,0.96j],[-0.96j,-0.28]])
v = m([[.6],[.8j]])
Qv = Q*v
print "Q= " ; Q.printf(); print
print "v= ",; v.printf(); print
print "Qv=",; Qv.printf(); print
print

