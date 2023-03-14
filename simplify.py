#!/usr/bin/env python

from sys import argv

try:
	from math import gcd
except ImportError:
	from fractions import gcd

try:
	from functools import reduce
except ImportError:
	pass

def mgcd(ns):
	ns = [abs(n) for n in ns if n]
	if ns:
		return reduce(gcd, ns)
	else:
		return 1

def simplify(ns):
	divisor = mgcd(ns)
	ns = [n // divisor for n in ns]
	return (ns, divisor)

def run_simplify(ns):
	ns, divisor = simplify(ns)
	print("GCD: " + str(divisor))
	print("Sim: " + " ".join(str(n) for n in ns))

def main():
	if len(argv) <= 1:
		print("usage: simplify <value> [<value> [...]]")
	else:
		try:
			ns = [int(a) for a in argv[1:]]
			run_simplify(ns)
		except:
			print("usage: simplify <value> [<value> [...]]")

if __name__ == "__main__": main()
