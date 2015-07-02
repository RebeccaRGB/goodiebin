#!/usr/bin/env python

from fractions import gcd
from sys import argv

def mgcd(ns):
	ns = map(abs, filter(None, ns))
	if ns:
		return reduce(gcd, ns)
	else:
		return 1

def simplify(ns):
	divisor = mgcd(ns)
	ns = map(lambda n: n // divisor, ns)
	return (ns, divisor)

def run_simplify(ns):
	ns, divisor = simplify(ns)
	print "GCD: " + str(divisor)
	print "Sim: " + " ".join(map(str, ns))

def main():
	if len(argv) <= 1:
		print "usage: simplify <value> [<value> [...]]"
	else:
		try:
			ns = map(int, argv[1:])
			run_simplify(ns)
		except:
			print "usage: simplify <value> [<value> [...]]"

if __name__ == "__main__": main()
