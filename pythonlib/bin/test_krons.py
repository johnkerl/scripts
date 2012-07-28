#!/usr/bin/python -Wall

from __future__ import division # 1/2 = 0.5, not 0.
from sackmat_m import *

I = m([[1, 0], [0, 1]])
A = m([[1, 2], [3, 4]])
u = [1,2]
v = [3,4]
w = [5,6]

print "================================================================"
print "A = "; print A
print

print "A tensor I = "; print A % I
print "I tensor A = "; print I % A
print

print "================================================================"
print "A tensor I tensor I = "; print multikron([A, I, I])
print "I tensor A tensor I = "; print multikron([I, A, I])
print "I tensor I tensor A = "; print multikron([I, I, A])
print

print "A tensor I tensor I = ";  print multikroni(A, 0, 3)
print "I tensor A tensor I = ";  print multikroni(A, 1, 3)
print "I tensor I tensor A = ";  print multikroni(A, 2, 3)
print

print "================================================================"
print "u                   = ",; print multivkron([u])
print "v                   = ",; print multivkron([v])
print "w                   = ",; print multivkron([w])
print "u tensor v          = ",; print multivkron([u, v])
print "u tensor v tensor w = ",; print multivkron([u, v, w])
print

print "================================================================"
print "I tensor A = ";                 print I%A;
print "Iu                        = ",; print I*u
print "Av                        = ",; print A*v
print "u tensor v                = ",; print vkron(u, v)
print "(Iu) tensor (Av)          = ",; print vkron(I*u, A*v)
print "(I tensor A) (u tensor v) = ",; print (I%A) * vkron(u, v)

