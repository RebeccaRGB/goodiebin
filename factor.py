#!/usr/bin/env python

from math import sqrt
from sys import argv
from time import time

try:
	from functools import reduce
except ImportError:
	pass

def factorize(n):
	if n < -1: return [(-1, 1)] + factorize(-n)
	elif n == -1: return [(-1, 1)]
	elif n == 0: return [(0, 1)]
	elif n == 1: return [(1, 1)]
	else:
		def potential_primes():
			base_primes = (2, 3, 5)
			for base_prime in base_primes:
				yield base_prime
			base_primes = (7, 11, 13, 17, 19, 23, 29, 31)
			prime_group = 0
			while True:
				for base_prime in base_primes:
					yield prime_group + base_prime
				prime_group += 30
		factors = []
		sqrtn = sqrt(n)
		for divisor in potential_primes():
			if divisor > sqrtn:
				break
			power = 0
			while (n % divisor) == 0:
				n //= divisor
				power += 1
			if power > 0:
				factors.append((divisor, power))
				sqrtn = sqrt(n)
		if n > 1:
			factors.append((n, 1))
		return factors

def divisors_from_factors(factors):
	def unsorted_divisors_from_factors(factors):
		if not factors: return [1]
		else:
			base, max_power = factors[0]
			if base == -1: return unsorted_divisors_from_factors(factors[1:])
			elif base == 0: return []
			elif base == 1: return unsorted_divisors_from_factors(factors[1:])
			else:
				divisors = unsorted_divisors_from_factors(factors[1:])
				all_divisors = []
				for power in range(0, max_power+1):
					all_divisors += map(lambda x: x * base ** power, divisors)
				return all_divisors
	all_divisors = unsorted_divisors_from_factors(factors)
	all_divisors.sort()
	return all_divisors


def test_factorize():
	start = time()
	n = 0
	while True:
		f = factorize(n)
		fa = map(lambda x: x[0] ** x[1], f)
		fb = reduce(lambda x,y: x * y, fa, 1)
		if fb != n:
			print("FACTORIZE FAILED AT " + str(n))
		d = divisors_from_factors(f)
		da = map(lambda x: d[x] * d[len(d)-x-1], range(0, len(d)))
		for db in da:
			if db != n:
				print("DIVISORS FAILED AT " + str(n))
		f = factorize(-n)
		fa = map(lambda x: x[0] ** x[1], f)
		fb = reduce(lambda x,y: x * y, fa, 1)
		if fb != -n:
			print("FACTORIZE FAILED AT " + str(-n))
		d = divisors_from_factors(f)
		da = map(lambda x: d[x] * d[len(d)-x-1], range(0, len(d)))
		for db in da:
			if db != n:
				print("DIVISORS FAILED AT " + str(-n))
		if (n % 10000) == 0:
			print("up to " + str(n) + " at " + str(time() - start) + "s")
		n += 1

def run_factorize(n):
	def str_from_factors_exp(factors):
		def str_from_factor(factor):
			if factor[1] == 1: return str(factor[0])
			else: return "^".join(map(str, factor))
		return " * ".join(map(str_from_factor, factors))
	def str_from_factors_mul(factors):
		factors = map(lambda x: [x[0]] * x[1], factors)
		factors = reduce(lambda x,y: x + y, factors, [])
		return " * ".join(map(str, factors))
	def pairs_from_divisors(d):
		return map(lambda x: (d[x], d[len(d)-x-1]), range(0, (1 + len(d)) // 2))
	def str_from_pairs(pairs):
		pairs = map(lambda x: "*".join(map(str, x)), pairs)
		return "0*0" if not pairs else "\t".join(pairs)
	f = factorize(n)
	print(str(n) + " = " + str_from_factors_exp(f))
	print(str(n) + " = " + str_from_factors_mul(f))
	print
	d = divisors_from_factors(f)
	print("Divisors: " + ("N/A" if not d else ", ".join(map(str, d))))
	s = reduce(lambda x,y: x + y, d, 0)
	sn = s - abs(n)
	s2n = sn - abs(n)
	ss = "zero" if s == 0 else "unit" if sn == 0 else "prime" if sn == 1 else "deficient" if s2n < 0 else "perfect" if s2n == 0 else "abundant"
	print("sigma_0(n) = " + str(len(d)))
	print("sigma_1(n) = " + str(s))
	print("sigma_1(n)-n = " + str(sn))
	print("sigma_1(n)-2n = " + str(s2n))
	print(str(abs(n)) + " is " + ss + ".")
	print
	p = pairs_from_divisors(d)
	print("Pairs:")
	print(str_from_pairs(p))


def main():
	if len(argv) <= 1:
		print("usage: factor <value> [<value> [...]]")
	else:
		for i in range(1, len(argv)):
			if i > 1: print
			if argv[i] == "test": test_factorize()
			else:
				try:
					n = int(argv[i])
					run_factorize(n)
				except:
					print(argv[i] + " is not an integer")

if __name__ == "__main__": main()
