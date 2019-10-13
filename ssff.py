#!/usr/bin/env python

import sys

def main():
	types = ''.join(sys.argv[1:]).upper()
	types = types.replace('S', ' ')
	types = types.replace('Q', '?')
	types = types.replace('E', '!')
	types = types.replace('T', '~')
	types = types.replace('Z', ' ACDIMRX?!~')
	if types:
		for line in sys.stdin:
			if line[0] in types:
				print(line[8:].strip())
	else:
		print('Usage: svn status | ssff <statuses>')
		print('Extracts file paths from status lines with the specified statuses.')

if __name__ == '__main__':
	main()
