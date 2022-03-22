#!/usr/bin/env python

from sys import argv
from sys import exit
from sys import stdout

def chargen(s, e, rm, cm, o, rc, cc, rd, cd):
	try:
		r = 0
		while r < rc or rc < 1:
			c = 0
			while c < cc or cc < 1:
				if c != 0:
					try:
						stdout.write(cd.encode('utf-8'))
					except TypeError:
						stdout.write(cd)
				cp = (rm * r + cm * c + o) % (e - s) + s
				try:
					stdout.write(unichr(cp).encode('utf-8'))
				except NameError:
					stdout.write(chr(cp))
				c += 1
			try:
				stdout.write(rd.encode('utf-8'))
			except TypeError:
				stdout.write(rd)
			r += 1
	except:
		pass

def parseord(s):
	try:
		return int(s, 0)
	except:
		try:
			return ord(s)
		except:
			print(s + " is not a single character")
			exit()

def parseint(s):
	try:
		return int(s, 0)
	except:
		print(s + " is not an integer")
		exit()

def parsechr(s):
	try:
		return unichr(int(s, 0))
	except:
		return s

def main():
	s = 32
	e = 127
	rm = 1
	cm = 1
	o = 1
	rc = 0
	cc = 72
	rd = u'\n'
	cd = u''
	i = 1
	while i < len(argv):
		arg = argv[i]
		i += 1
		if arg == "--help":
			print("usage: chargen [<option> [<value>] [...]]")
			print("   -sc <uni>   -s <uni>   start character (-sc <x> is the same as -fc <x>)")
			print("   -ec <uni>   -e <uni>   end character (-ec <x> is the same as -lc <x-1>)")
			print("   -fc <uni>   -f <uni>   first character (-fc <x> is the same as -sc <x>)")
			print("   -lc <uni>   -l <uni>   last character (-lc <x> is the same as -ec <x+1>)")
			print("   -rm <int>   -y <int>   difference in code point value between lines")
			print("   -cm <int>   -x <int>   difference in code point value between columns")
			print("   -so <int>   -o <int>   first character to print relative to start character")
			print("   -rc <int>   -n <int>   number of lines to print")
			print("   -cc <int>   -w <int>   number of columns to print")
			print("   -hc         -h         print horizontal chart (sets -rm, -cm, -so, -rc, -cc)")
			print("   -vc         -v         print vertical chart (sets -rm, -cm, -so, -rc, -cc)")
			print("   -rd <str>   -r <str>   string to print between lines (default is newline)")
			print("   -cd <str>   -t <str>   string to print between columns (default is empty)")
			exit()
		elif (arg == "-sc" or arg == "-s") and i < len(argv):
			s = parseord(argv[i])
			o = 0
			i += 1
		elif (arg == "-ec" or arg == "-e") and i < len(argv):
			e = parseord(argv[i])
			o = 0
			i += 1
		elif (arg == "-fc" or arg == "-f") and i < len(argv):
			s = parseord(argv[i])
			o = 0
			i += 1
		elif (arg == "-lc" or arg == "-l") and i < len(argv):
			e = parseord(argv[i]) + 1
			o = 0
			i += 1
		elif (arg == "-rm" or arg == "-y") and i < len(argv):
			rm = parseint(argv[i])
			o = 0
			i += 1
		elif (arg == "-cm" or arg == "-x") and i < len(argv):
			cm = parseint(argv[i])
			o = 0
			i += 1
		elif (arg == "-so" or arg == "-o") and i < len(argv):
			o = parseint(argv[i])
			i += 1
		elif (arg == "-rc" or arg == "-n") and i < len(argv):
			rc = parseint(argv[i])
			i += 1
		elif (arg == "-cc" or arg == "-w") and i < len(argv):
			cc = parseint(argv[i])
			i += 1
		elif (arg == "-hc" or arg == "-h"):
			rm = 1
			cm = 16
			o = 0
			rc = 16
			cc = ((e - s) + 15) >> 4
		elif (arg == "-vc" or arg == "-v"):
			rm = 16
			cm = 1
			o = 0
			rc = ((e - s) + 15) >> 4
			cc = 16
		elif (arg == "-rd" or arg == "-r") and i < len(argv):
			rd = parsechr(argv[i])
			i += 1
		elif (arg == "-cd" or arg == "-t") and i < len(argv):
			cd = parsechr(argv[i])
			i += 1
		else:
			print("Unknown option: " + arg)
			exit()
	chargen(s, e, rm, cm, o, rc, cc, rd, cd)

if __name__ == "__main__": main()
