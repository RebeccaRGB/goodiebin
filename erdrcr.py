#!/usr/bin/env python

from struct import pack
from struct import unpack
from sys import argv
from sys import exit

def help():
	print ("erdrcr - ErroR DetectoR and CorrectoR for binary files")
	print ("usage: erdrcr [<paths>] [-o <path>]")
	print ("   -i <path>   specify binary files to compare")
	print ("   -o <path>   specify file to write corrected data to")

def erdrcr(input, output):
	# Open Files
	input = [open(f, "rb") for f in input]
	if output is not None:
		output = open(output, "wb")
	# Compare
	addr = 0
	errs = 0
	fatal = 0
	while True:
		bytes = [f.read(1) for f in input]
		if all(len(b) == 0 for b in bytes):
			break
		else:
			bytes = [(unpack("B", b)[0] if len(b) > 0 else 0) for b in bytes]
			byte = bytes[0]
			bytes = [format(b, "08b") for b in bytes]
			for i in range(0, 8):
				bits = [b[i] for b in bytes]
				zeroes = bits.count("0")
				ones = bits.count("1")
				if zeroes > 0 and ones > 0:
					mask = 0x80 >> i
					if zeroes > ones:
						correction = "0"
						byte &=~ mask
					elif ones > zeroes:
						correction = "1"
						byte |= mask
					else:
						correction = "?"
						fatal += 1
					if errs == 0:
						print ("Address.Mask\t0's\t1's\tCorrection")
					print ("{0:08X}.{1:02X}:\t{2}\t{3}\t{4}".format(addr, mask, zeroes, ones, correction))
					errs += 1
			if output is not None:
				output.write(pack("B", byte))
			addr += 1
	# Close Files
	[f.close() for f in input]
	if output is not None:
		output.close()
	# Report
	if errs > 0:
		percent = 100.0 * errs / (addr << 3)
		print ("{0} out of {1} bits mismatched ({2}% error rate)".format(errs, addr << 3, percent))
		if fatal > 0:
			percent = 100.0 * fatal / (addr << 3)
			print ("{0} out of {1} bits unrecoverable ({2}% error rate)".format(fatal, addr << 3, percent))
		else:
			print ("all errors correctable")
		return 1
	else:
		print ("no differences found")
		return 0

def main():
	input = []
	output = None
	i = 1
	while i < len(argv):
		arg = argv[i]
		i += 1
		if arg == "--help":
			help()
			exit()
		elif arg == "-i" and i < len(argv):
			input.append(argv[i])
			i += 1
		elif arg == "-o" and i < len(argv):
			output = argv[i]
			i += 1
		else:
			input.append(arg)
	if len(input) == 0:
		help()
	else:
		exit(erdrcr(input, output))

if __name__ == "__main__": main()
