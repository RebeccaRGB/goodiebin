#!/usr/bin/env python

from sys import argv

def approximate(n, m):
	if n < 0.0:
		num, den, val, dif, err = approximate(-n, m)
		return (-num, den, -val, dif, err)
	elif n == 0.0:
		return (0, 1, 0.0, 0.0, 0.0)
	else:
		best_num = 1
		best_den = 1
		best_val = 1.0
		best_dif = abs(1.0 - n)
		best_err = best_dif / n
		for den in xrange(1, m + 1):
			num = int(round(n * float(den)))
			val = float(num) / float(den)
			dif = abs(val - n)
			err = dif / n
			if (dif < best_dif):
				best_num = num
				best_den = den
				best_val = val
				best_dif = dif
				best_err = err
		return (best_num, best_den, best_val, best_dif, best_err)

def run_approximate(n, m):
	num, den, val, dif, err = approximate(n, m)
	print str(n) + u' \u2248 ' + str(num) + " / " + str(den) + " = " + str(val)
	print "Delta: " + str(dif)
	print "Error: " + str(err * 100.0) + "%"

def main():
	if len(argv) <= 2:
		print "usage: approximate <highest-denominator> <value> [<value> [...]]"
	else:
		try:
			mm = max(1, abs(int(argv[1])))
			for i in xrange(2, len(argv)):
				if i > 2: print
				try:
					n = float(argv[i])
					run_approximate(n, mm)
				except:
					print argv[i] + " is not a number"
		except:
			print argv[1] + " is not an integer"

if __name__ == "__main__": main()
