#!/usr/bin/env python

from math import floor
from sys import argv

def floatbase(s, b):
	sawsign = False
	sawdp = False
	sign = +1
	man = 0
	exp = 0
	for ch in s:
		if ch == '+' and not sawsign:
			sawsign = True
			sign = +1
		elif ch == '-' and not sawsign:
			sawsign = True
			sign = -1
		elif ch == '.' and not sawdp:
			sawsign = True
			sawdp = True
		else:
			sawsign = True
			digit = int(ch, b)
			man = man * b + digit
			if sawdp: exp += 1
	return float(sign * man) / (float(b) ** float(exp))

def strbase(n, b):
	if n < 0:
		return "-" + strbase(-n, b)
	else:
		def strdigit(d):
			return chr(48 + d) if d < 10 else chr(55 + d)
		ip = floor(n)
		fp = n - ip
		ips = ""
		fps = ""
		while ip > 0:
			(ip, digit) = divmod(ip, b)
			ips = strdigit(int(digit)) + ips
		while fp > 0:
			fp *= b
			digit = floor(fp)
			fp -= digit
			fps = fps + strdigit(int(digit))
		if ips == "": ips = "0"
		return ips if fps == "" else ips + "." + fps

def main():
	if len(argv) <= 3:
		print("usage: bcr <input-radix> <output-radix> <value> [<value> [...]]")
		return
	try:
		sb = int(argv[1])
		if sb < 2 or sb > 36:
			print("input radix out of range: " + str(sb))
			return
	except:
		print("input radix not an integer: " + argv[1])
		return
	try:
		db = int(argv[2])
		if db < 2 or db > 36:
			print("output radix out of range: " + str(db))
			return
	except:
		print("output radix not an integer: " + argv[2])
		return
	for i in range(3, len(argv)):
		try:
			n = floatbase(argv[i], sb)
			dn = strbase(n, db)
			print(dn)
		except:
			print("invalid value: " + argv[i])

if __name__ == "__main__": main()
