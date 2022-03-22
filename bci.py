#!/usr/bin/env python

from sys import argv

def strbase(n, b):
	if n < 0:
		return "-" + strbase(-n, b)
	else:
		(d, m) = divmod(n, b)
		ms = chr(48 + m) if m < 10 else chr(55 + m)
		return strbase(d, b) + ms if d > 0 else ms

def main():
	if len(argv) <= 3:
		print("usage: bci <input-radix> <output-radix> <value> [<value> [...]]")
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
			n = int(argv[i], sb)
			dn = strbase(n, db)
			print(dn)
		except:
			print("invalid value: " + argv[i])

if __name__ == "__main__": main()
