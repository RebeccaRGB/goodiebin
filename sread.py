#!/usr/bin/env python

from __future__ import print_function
import serial
import time
from sys import argv
from sys import exit
from sys import stderr
from sys import stdout

def help():
	print("usage: sread [<options>] <device> [<output>]", file=stderr)
	print("   -u <path>   serial device to read from", file=stderr)
	print("   -b <int>    baud rate", file=stderr)
	print("   -d <int>    data bits (5, 6, 7, 8)", file=stderr)
	print("   -p <str>    parity (none, even, odd, mark, space)", file=stderr)
	print("   -s <num>    stop bits (1, 1.5, 2)", file=stderr)
	print("   -t <num>    timeout (seconds)", file=stderr)
	print("   -x          enable XON/XOFF", file=stderr)
	print("   -r          enable RTS/CTS", file=stderr)
	print("   -h          enable DSR/DTR", file=stderr)
	print("   -o <path>   path to write to", file=stderr)
	print("   -w <num>    delay before reading (seconds)", file=stderr)
	print("   -l <int>    number of bytes to read", file=stderr)

def main():
	port = None
	baudrate = 9600
	bytesize = serial.EIGHTBITS
	parity = serial.PARITY_NONE
	stopbits = serial.STOPBITS_ONE
	timeout = None
	xonxoff = False
	rtscts = False
	dsrdtr = False
	output = None
	delay = None
	length = None
	i = 1
	while i < len(argv):
		arg = argv[i]
		i += 1
		if arg == "--help":
			help()
			exit()
		elif arg == "-u" and i < len(argv):
			port = argv[i]
			i += 1
		elif arg == "-b" and i < len(argv):
			try:
				baudrate = int(argv[i])
			except:
				print(argv[i] + " is not valid for -b", file=stderr)
				exit()
			i += 1
		elif arg == "-d" and i < len(argv):
			if argv[i] == "5":
				bytesize = serial.FIVEBITS
			elif argv[i] == "6":
				bytesize = serial.SIXBITS
			elif argv[i] == "7":
				bytesize = serial.SEVENBITS
			elif argv[i] == "8":
				bytesize = serial.EIGHTBITS
			else:
				print(argv[i] + " is not valid for -d", file=stderr)
				exit()
			i += 1
		elif arg == "-p" and i < len(argv):
			if argv[i] == "N" or argv[i] == "n" or argv[i] == "none":
				parity = serial.PARITY_NONE
			elif argv[i] == "E" or argv[i] == "e" or argv[i] == "even":
				parity = serial.PARITY_EVEN
			elif argv[i] == "O" or argv[i] == "o" or argv[i] == "odd":
				parity = serial.PARITY_ODD
			elif argv[i] == "M" or argv[i] == "m" or argv[i] == "mark":
				parity = serial.PARITY_MARK
			elif argv[i] == "S" or argv[i] == "s" or argv[i] == "space":
				parity = serial.PARITY_SPACE
			else:
				print(argv[i] + " is not valid for -p", file=stderr)
				exit()
			i += 1
		elif arg == "-s" and i < len(argv):
			if argv[i] == "1":
				stopbits = serial.STOPBITS_ONE
			elif argv[i] == "1.5":
				stopbits = serial.STOPBITS_ONE_POINT_FIVE
			elif argv[i] == "2":
				stopbits = serial.STOPBITS_TWO
			else:
				print(argv[i] + " is not valid for -s", file=stderr)
				exit()
			i += 1
		elif arg == "-t" and i < len(argv):
			try:
				timeout = float(argv[i])
			except:
				print(argv[i] + " is not valid for -t", file=stderr)
				exit()
			i += 1
		elif arg == "-x":
			xonxoff = True
		elif arg == "-X":
			xonxoff = False
		elif arg == "-r":
			rtscts = True
		elif arg == "-R":
			rtscts = False
		elif arg == "-h":
			dsrdtr = True
		elif arg == "-H":
			dsrdtr = False
		elif arg == "-o" and i < len(argv):
			output = argv[i]
			i += 1
		elif arg == "-w" and i < len(argv):
			try:
				delay = float(argv[i])
			except:
				print(argv[i] + " is not valid for -w", file=stderr)
				exit()
			i += 1
		elif arg == "-l" and i < len(argv):
			try:
				length = int(argv[i])
			except:
				print(argv[i] + " is not valid for -l", file=stderr)
				exit()
			i += 1
		elif port is None:
			port = arg
		elif output is None:
			output = arg
		else:
			help()
			exit()
	if port is None:
		help()
	else:
		try:
			if output is None:
				with serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize,
								   parity=parity, stopbits=stopbits, timeout=timeout,
								   xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr) as ser:
					if delay is not None:
						time.sleep(delay)
					i = 0
					while length is None or i < length:
						b = ser.read(1)
						stdout.write(b)
						i += len(b)
			else:
				with open(output, "w") as f:
					with serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize,
									   parity=parity, stopbits=stopbits, timeout=timeout,
									   xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr) as ser:
						if delay is not None:
							time.sleep(delay)
						i = 0
						while length is None or i < length:
							b = ser.read(1)
							f.write(b)
							i += len(b)
		except KeyboardInterrupt:
			pass

if __name__ == "__main__": main()
