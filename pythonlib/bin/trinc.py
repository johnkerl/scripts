#!/usr/bin/python -Wall


from kerlutil import fact

n = 6
for a in range(0, n+1):
	for b in range(0, n+1):
		c = n - a - b
		if c < 0:
			continue
		t = fact(n) / fact(a) / fact(b) / fact(c)
		print "n=%d a=%d b=%d c=%d n!=%d a!=%d b!=%d c!=%d t=%d" \
			% (n, a, b, c, fact(n), fact(a), fact(b), fact(c), t)
		#print t,
	print
