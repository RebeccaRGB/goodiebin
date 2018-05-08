#!/usr/bin/env python
#coding=utf8

import math
import random
import re
import sys



bin_pattern = '(?P<bin>(0[Bb](?P<binmag>([01]+([.][01]*)?|[.][01]+))))'
oct_pattern = '(?P<oct>(0[Oo](?P<octmag>([0-7]+([.][0-7]*)?|[.][0-7]+))))'
doz_pattern = '(?P<doz>(0[Dd](?P<dozmag>([0-9AaBbEeTtXx]+([.][0-9AaBbEeTtXx]*)?|[.][0-9AaBbEeTtXx]+))))'
hex_pattern = '(?P<hex>(0[HhXx](?P<hexmag>([0-9A-Fa-f]+([.][0-9A-Fa-f]*)?|[.][0-9A-Fa-f]+))))'
rad_pattern = '(?P<rad>((?P<radrad>([0-9]+))[Rr](?P<radmag>([0-9A-Za-z]+([.][0-9A-Za-z]*)?|[.][0-9A-Za-z]+))))'
dec_pattern = '(?P<dec>([0-9]+([.][0-9]*)?|[.][0-9]+))'
mag_pattern = '(' + '|'.join([bin_pattern, oct_pattern, doz_pattern, hex_pattern, rad_pattern, dec_pattern]) + ')'
binexp_pattern = '(?P<binexp>([Bb](?P<binexpexp>([+-]?[0-9]+))))'
decexp_pattern = '(?P<decexp>([Ee](?P<decexpexp>([+-]?[0-9]+))))'
exp_pattern = '(?P<exp>((' + '|'.join([binexp_pattern, decexp_pattern]) + ')?))'
value_pattern = re.compile(mag_pattern + exp_pattern)
id_pattern = re.compile('[A-Za-z][A-Za-z0-9]*')



ops_map = {
	'!': (0, ':NOT:'),
	'~': (0, ':BITNOT:'),
	'¬': (0, ':NOT:'),
	'∛': (0, ':CBRT:'),
	'∜': (0, ':QTRT:'),
	':N': (0, ':NOT:'),
	':n': (0, ':BITNOT:'),
	':C': (0, ':CBRT:'),
	':c': (0, ':CBRT:'),
	':Q': (0, ':QTRT:'),
	':q': (0, ':QTRT:'),
	'**': (1, ':EXP:'),
	'^': (1, ':EXP:'),
	'_': (1, ':LOG:'),
	'↑': (1, ':EXP:'),
	'↓': (1, ':LOG:'),
	'√': (1, ':ROOT:'),
	':E': (1, ':EXP:'),
	':e': (1, ':EXP:'),
	':G': (1, ':LOG:'),
	':g': (1, ':LOG:'),
	':V': (1, ':ROOT:'),
	':v': (1, ':ROOT:'),
	'*': (2, ':MUL:'),
	'/': (2, ':DIV:'),
	'\\': (2, ':QUO:'),
	'%': (2, ':REM:'),
	'×': (2, ':MUL:'),
	'·': (2, ':MUL:'),
	'÷': (2, ':DIV:'),
	':M': (2, ':MUL:'),
	':m': (2, ':MUL:'),
	':/': (2, ':QUO:'),
	'+': (3, ':ADD:'),
	'-': (3, ':SUB:'),
	'<<': (4, ':LSH:'),
	'<<<': (4, ':LSH:'),
	'>>': (4, ':RSH:'),
	'>>>': (4, ':RSH:'),
	':[[': (4, ':LSH:'),
	':[[[': (4, ':LSH:'),
	':]]': (4, ':RSH:'),
	':]]]': (4, ':RSH:'),
	':L': (4, ':LSH:'),
	':l': (4, ':LSH:'),
	':R': (4, ':RSH:'),
	':r': (4, ':RSH:'),
	'&': (5, ':BITAND:'),
	':a': (5, ':BITAND:'),
	'#': (6, ':BITXOR:'),
	':x': (6, ':BITXOR:'),
	'|': (7, ':BITOR:'),
	':o': (7, ':BITOR:'),
	'<': (8, ':LT:'),
	'>': (8, ':GT:'),
	'<=': (8, ':LE:'),
	'>=': (8, ':GE:'),
	'=<': (8, ':LE:'),
	'=>': (8, ':GE:'),
	'≤': (8, ':LE:'),
	'≥': (8, ':GE:'),
	':[': (8, ':LT:'),
	':]': (8, ':GT:'),
	':[=': (8, ':LE:'),
	':]=': (8, ':GE:'),
	':=[': (8, ':LE:'),
	':=]': (8, ':GE:'),
	'=': (9, ':EQ:'),
	'==': (9, ':EQ:'),
	'===': (9, ':EQ:'),
	'<>': (9, ':NE:'),
	'!=': (9, ':NE:'),
	'!==': (9, ':NE:'),
	'≠': (9, ':NE:'),
	'≠≠': (9, ':NE:'),
	'≠≠≠': (9, ':NE:'),
	':[]': (9, ':NE:'),
	':/=': (9, ':NE:'),
	':=/': (9, ':NE:'),
	'<=>': (9, ':CMP:'),
	'⇔': (9, ':CMP:'),
	':[=]': (9, ':CMP:'),
	'&&': (10, ':AND:'),
	':A': (10, ':AND:'),
	'##': (11, ':XOR:'),
	':X': (11, ':XOR:'),
	'||': (12, ':OR:'),
	':O': (12, ':OR:'),
	':': (13, ':LET:'),
	':=': (13, ':LET:'),
	':==': (13, ':LET:'),
	'←': (13, ':LET:'),
	'(': (14, ':LP:'),
	')': (14, ':RP:'),
	'[': (14, ':LP:'),
	']': (14, ':RP:'),
	',': (15, ':EOA:'),
	';': (16, ':EOS:'),
	'::': (16, ':EOS:'),
}

ops = ops_map.keys()
ops.sort()
ops.sort(key=len, reverse=True)



consts = {
	'e': math.e,
	'euler': math.e,
	'pi': math.pi,
	'phi': (math.sqrt(5) + 1) / 2,
	'tau': math.pi * 2,
	'NAN': float('nan'),
	'NaN': float('nan'),
	'nan': float('nan'),
	'INF': float('inf'),
	'Inf': float('inf'),
	'inf': float('inf'),
	'INFTY': float('inf'),
	'Infty': float('inf'),
	'infty': float('inf'),
	'INFINITY': float('inf'),
	'Infinity': float('inf'),
	'infinity': float('inf'),
	'FALSE': False,
	'False': False,
	'false': False,
	'TRUE': True,
	'True': True,
	'true': True,
}



def signum(x):
	if x == 0:
		return 0
	elif x > 0:
		return 1
	elif x < 0:
		return -1
	else:
		return float('nan')

def rsr(*args):
	for a in args:
		if a == 0.0:
			return 0.0
	return 1.0 / math.fsum(1.0 / a for a in args)

def rms(*args):
	data = list(args)
	return math.sqrt(math.fsum(x * x for x in data) / len(data))

def average(*args):
	data = list(args)
	return math.fsum(data) / len(data)

def geomean(*args):
	data = list(args)
	p = reduce(lambda x, y: x * y, data, 1)
	return math.pow(p, 1.0 / len(data))

def svariance(*args):
	data = list(args)
	avg = math.fsum(data) / len(data)
	ssd = math.fsum((x - avg) ** 2 for x in data)
	return ssd / (len(data) - 1)

def pvariance(*args):
	data = list(args)
	avg = math.fsum(data) / len(data)
	ssd = math.fsum((x - avg) ** 2 for x in data)
	return ssd / len(data)

def sstddev(*args):
	return math.sqrt(svariance(*args))

def pstddev(*args):
	return math.sqrt(pvariance(*args))

def median(*args):
	data = list(args)
	data.sort()
	if len(data) % 2 == 1:
		return data[len(data) / 2]
	else:
		a = float(data[len(data) / 2 - 1])
		b = float(data[len(data) / 2])
		return (a + b) / 2

def agm(a, b):
	if math.isnan(a): return a
	if math.isnan(b): return b
	while a != b: a, b = (a + b) / 2.0, math.sqrt(a * b)
	return a

def gcd(a, b):
	if math.isnan(a): return a
	if math.isnan(b): return b
	while b != 0: a, b = b, a % b
	return a

def lcm(a, b):
	return a / gcd(a, b) * b

def reversebits(v, w):
	if not isinstance(v, (int, long)):
		raise ValueError('reversebits requires integer arguments')
	if not isinstance(w, (int, long)):
		raise ValueError('reversebits requires integer arguments')

	r = (-1 << w) if (v & 1) else 0
	ma = (1 << (w - 1))
	mb = 1
	for i in range(0, w):
		if v & ma: r |= mb
		ma >>= 1
		mb <<= 1
	return r

def reversebytes(v, w):
	if not isinstance(v, (int, long)):
		raise ValueError('reversebytes requires integer arguments')
	if not isinstance(w, (int, long)):
		raise ValueError('reversebytes requires integer arguments')

	r = (-1 << (w << 3)) if (v & 0x80) else 0
	sa = ((w - 1) << 3)
	sb = 0
	for i in range(0, w):
		r |= (((v >> sa) & 0xFF) << sb)
		sa -= 8
		sb += 8
	return r

def bitlength(x):
	if not isinstance(x, (int, long)):
		raise ValueError('bitlength requires integer arguments')

	r = 0
	while not (x == 0 or x == -1):
		r += 1
		x >>= 1
	return r

def bitmingle(a, b):
	if not isinstance(a, (int, long)):
		raise ValueError('bitmingle requires integer arguments')
	if not isinstance(b, (int, long)):
		raise ValueError('bitmingle requires integer arguments')

	n = max(bitlength(a), bitlength(b))
	if a < 0 and b < 0:
		c = (-1 << (n << 1))
	elif a < 0 or b < 0:
		raise ValueError('math domain error')
	else:
		c = 0
	for i in range(0, n):
		if b & (1 << i):
			c |= (1 << (i + i))
		if a & (1 << i):
			c |= (1 << (i + i + 1))
	return c

def bitselect(a, b):
	if not isinstance(a, (int, long)):
		raise ValueError('bitselect requires integer arguments')
	if not isinstance(b, (int, long)):
		raise ValueError('bitselect requires integer arguments')

	n = max(bitlength(a), bitlength(b))
	c = 0
	ci = 0
	for i in range(0, n):
		if b & (1 << i):
			if a & (1 << i):
				c |= (1 << ci)
			ci += 1
	if a < 0 and b < 0:
		c |= (-1 << ci)
	return c

def gamma(z):
	try:
		return math.gamma(z)
	except:
		if z <= 0 and math.ceil(z) == z:
			raise ValueError('math domain error')
		elif z == 1 or z == 2:
			return 1.0
		elif math.isinf(z):
			return z
		elif z < 0.5:
			return math.pi / (math.sin(math.pi * z) * gamma(1.0 - z))
		else:
			G = 7
			P = [
				0.99999999999980993,
				676.5203681218851,
				-1259.1392167224028,
				771.32342877765313,
				-176.61502916214059,
				12.507343278686905,
				-0.13857109526572012,
				9.9843695780195716e-6,
				1.5056327351493116e-7
			]
			z -= 1.0
			x = P[0]
			for i in range(1, G + 2):
				x += P[i] / (z + i)
			t = z + G + 0.5
			return math.sqrt(math.pi * 2) * math.pow(t, z + 0.5) * math.exp(-t) * x

def lgamma(z):
	try:
		return math.lgamma(z)
	except:
		return math.log(gamma(z))



def func_wrap(fn):
	def wrapper(e, args):
		rv = fn(*[a['value'] for a in args])
		rr = args[0]['radix'] if len(args) > 0 else 0
		return {'type': 'value', 'image': e['image'], 'value': rv, 'radix': rr}
	return wrapper

def func_iterwrap(fn):
	def wrapper(e, args):
		rv = fn(a['value'] for a in args)
		rr = args[0]['radix'] if len(args) > 0 else 0
		return {'type': 'value', 'image': e['image'], 'value': rv, 'radix': rr}
	return wrapper

def func_reduce(fn, dr):
	def wrapper(e, args):
		rv = reduce(fn, [a['value'] for a in args], dr)
		rr = args[0]['radix'] if len(args) > 0 else 0
		return {'type': 'value', 'image': e['image'], 'value': rv, 'radix': rr}
	return wrapper

def func_forallpairs(fn):
	def wrapper(e, args):
		rv = all(fn(args[i]['value'], args[i + 1]['value']) for i in range(0, len(args) - 1))
		rr = args[0]['radix'] if len(args) > 0 else 0
		return {'type': 'value', 'image': e['image'], 'value': rv, 'radix': rr}
	return wrapper

def func_radix(r):
	def wrapper(e, args):
		args[0]['radix'] = r
		return args[0]
	return wrapper

funcs = {
	'abs': (1, 1, func_wrap(abs)),
	'sgn': (1, 1, func_wrap(signum)),
	'sign': (1, 1, func_wrap(signum)),
	'signum': (1, 1, func_wrap(signum)),
	'sqrt': (1, 1, func_wrap(math.sqrt)),
	'cbrt': (1, 1, func_wrap(lambda x: math.pow(x, 1.0/3.0))),
	'qtrt': (1, 1, func_wrap(lambda x: math.sqrt(math.sqrt(x)))),
	'toDegrees': (1, 1, func_wrap(math.degrees)),
	'toRadians': (1, 1, func_wrap(math.radians)),
	'todegrees': (1, 1, func_wrap(math.degrees)),
	'toradians': (1, 1, func_wrap(math.radians)),
	'degrees': (1, 1, func_wrap(math.degrees)),
	'radians': (1, 1, func_wrap(math.radians)),
	'toDeg': (1, 1, func_wrap(math.degrees)),
	'toRad': (1, 1, func_wrap(math.radians)),
	'todeg': (1, 1, func_wrap(math.degrees)),
	'torad': (1, 1, func_wrap(math.radians)),
	'isFinite': (1, 1, func_wrap(lambda x: not (math.isinf(x) or math.isnan(x)))),
	'isfinite': (1, 1, func_wrap(lambda x: not (math.isinf(x) or math.isnan(x)))),
	'isInfinite': (1, 1, func_wrap(math.isinf)),
	'isinfinite': (1, 1, func_wrap(math.isinf)),
	'isInf': (1, 1, func_wrap(math.isinf)),
	'isinf': (1, 1, func_wrap(math.isinf)),
	'isNaN': (1, 1, func_wrap(math.isnan)),
	'isnan': (1, 1, func_wrap(math.isnan)),
	'sum': (0, 0, func_iterwrap(sum)),
	'prod': (0, 0, func_reduce(lambda x, y: x * y, 1)),
	'product': (0, 0, func_reduce(lambda x, y: x * y, 1)),
	'rsr': (0, 0, func_wrap(rsr)),
	'rms': (0, 0, func_wrap(rms)),
	'random': (1, 1, func_wrap(lambda x: random.randint(1, x))),
	'randomRange': (2, 2, func_wrap(random.randint)),
	'randomrange': (2, 2, func_wrap(random.randint)),
	'randomDecimal': (1, 1, func_wrap(lambda x: (1 - random.random()) * x)),
	'randomdecimal': (1, 1, func_wrap(lambda x: (1 - random.random()) * x)),
	'ceil': (1, 1, func_wrap(math.ceil)),
	'floor': (1, 1, func_wrap(math.floor)),
	'aug': (1, 1, func_wrap(lambda x: math.floor(x) if x < 0 else math.ceil(x))),
	'trunc': (1, 1, func_wrap(lambda x: math.ceil(x) if x < 0 else math.floor(x))),
	'round': (1, 2, func_wrap(round)),
	'rint': (1, 2, func_wrap(round)),
	'int': (1, 1, func_wrap(int)),
	'frac': (1, 1, func_wrap(lambda x: x - int(x))),
	'exp': (1, 1, func_wrap(math.exp)),
	'exp1': (1, 1, func_wrap(math.expm1)),
	'expm1': (1, 1, func_wrap(math.expm1)),
	'exp2': (1, 1, func_wrap(lambda x: 2 ** x)),
	'exp10': (1, 1, func_wrap(lambda x: 10 ** x)),
	'ln': (1, 1, func_wrap(math.log)),
	'ln1': (1, 1, func_wrap(math.log1p)),
	'ln1p': (1, 1, func_wrap(math.log1p)),
	'log': (1, 2, func_wrap(math.log)),
	'log1': (1, 1, func_wrap(math.log1p)),
	'log1p': (1, 1, func_wrap(math.log1p)),
	'log2': (1, 1, func_wrap(lambda x: math.log(x, 2))),
	'log10': (1, 1, func_wrap(math.log10)),
	'pow': (2, 2, func_wrap(math.pow)),
	'root': (2, 2, func_wrap(lambda x, y: math.pow(x, 1.0 / y))),
	'sin': (1, 1, func_wrap(math.sin)),
	'cos': (1, 1, func_wrap(math.cos)),
	'tan': (1, 1, func_wrap(math.tan)),
	'cot': (1, 1, func_wrap(lambda x: 1.0 / math.tan(x))),
	'sec': (1, 1, func_wrap(lambda x: 1.0 / math.cos(x))),
	'csc': (1, 1, func_wrap(lambda x: 1.0 / math.sin(x))),
	'asin': (1, 1, func_wrap(math.asin)),
	'acos': (1, 1, func_wrap(math.acos)),
	'atan': (1, 1, func_wrap(math.atan)),
	'acot': (1, 1, func_wrap(lambda x: math.atan(1.0 / x))),
	'asec': (1, 1, func_wrap(lambda x: math.acos(1.0 / x))),
	'acsc': (1, 1, func_wrap(lambda x: math.asin(1.0 / x))),
	'sinh': (1, 1, func_wrap(math.sinh)),
	'cosh': (1, 1, func_wrap(math.cosh)),
	'tanh': (1, 1, func_wrap(math.tanh)),
	'coth': (1, 1, func_wrap(lambda x: 1.0 / math.tanh(x))),
	'sech': (1, 1, func_wrap(lambda x: 1.0 / math.cosh(x))),
	'csch': (1, 1, func_wrap(lambda x: 1.0 / math.sinh(x))),
	'asinh': (1, 1, func_wrap(math.asinh)),
	'acosh': (1, 1, func_wrap(math.acosh)),
	'atanh': (1, 1, func_wrap(math.atanh)),
	'acoth': (1, 1, func_wrap(lambda x: math.atanh(1.0 / x))),
	'asech': (1, 1, func_wrap(lambda x: math.acosh(1.0 / x))),
	'acsch': (1, 1, func_wrap(lambda x: math.asinh(1.0 / x))),
	'hypot': (2, 2, func_wrap(math.hypot)),
	'atan2': (2, 2, func_wrap(math.atan2)),
	'radius': (2, 2, func_wrap(math.hypot)),
	'theta': (2, 2, func_wrap(lambda x, y: math.atan2(y, x))),
	'xcoord': (2, 2, func_wrap(lambda r, t: r * math.cos(t))),
	'ycoord': (2, 2, func_wrap(lambda r, t: r * math.sin(t))),
	'avg': (0, 0, func_wrap(average)),
	'geom': (0, 0, func_wrap(geomean)),
	'average': (0, 0, func_wrap(average)),
	'geomean': (0, 0, func_wrap(geomean)),
	'min': (0, 0, func_iterwrap(min)),
	'max': (0, 0, func_iterwrap(max)),
	'minimum': (0, 0, func_iterwrap(min)),
	'maximum': (0, 0, func_iterwrap(max)),
	'stddev': (0, 0, func_wrap(pstddev)),
	'pstddev': (0, 0, func_wrap(pstddev)),
	'sstddev': (0, 0, func_wrap(sstddev)),
	'variance': (0, 0, func_wrap(pvariance)),
	'pvariance': (0, 0, func_wrap(pvariance)),
	'svariance': (0, 0, func_wrap(svariance)),
	'annuity': (2, 2, func_wrap(lambda r, p: (1 - ((1 + r) ** (-p))) / r)),
	'compound': (2, 2, func_wrap(lambda r, p: (1 + r) ** p)),
	'fact': (1, 1, func_wrap(lambda x: gamma(x + 1))),
	'lfact': (1, 1, func_wrap(lambda x: lgamma(x + 1))),
	'lnfact': (1, 1, func_wrap(lambda x: lgamma(x + 1))),
	'factorial': (1, 1, func_wrap(lambda x: gamma(x + 1))),
	'lfactorial': (1, 1, func_wrap(lambda x: lgamma(x + 1))),
	'lnfactorial': (1, 1, func_wrap(lambda x: lgamma(x + 1))),
	'gamma': (1, 1, func_wrap(gamma)),
	'lgamma': (1, 1, func_wrap(lgamma)),
	'lngamma': (1, 1, func_wrap(lgamma)),
	'beta': (2, 2, func_wrap(lambda x, y: gamma(x) * gamma(y) / gamma(x + y))),
	'lbeta': (2, 2, func_wrap(lambda x, y: lgamma(x) + lgamma(y) - lgamma(x + y))),
	'lnbeta': (2, 2, func_wrap(lambda x, y: lgamma(x) + lgamma(y) - lgamma(x + y))),
	'nCr': (2, 2, func_wrap(lambda n, r: gamma(n + 1) / (gamma(r + 1) * gamma(n - r + 1)))),
	'ncr': (2, 2, func_wrap(lambda n, r: gamma(n + 1) / (gamma(r + 1) * gamma(n - r + 1)))),
	'choose': (2, 2, func_wrap(lambda n, r: gamma(n + 1) / (gamma(r + 1) * gamma(n - r + 1)))),
	'nPr': (2, 2, func_wrap(lambda n, r: gamma(n + 1) / gamma(n - r + 1))),
	'npr': (2, 2, func_wrap(lambda n, r: gamma(n + 1) / gamma(n - r + 1))),
	'pick': (2, 2, func_wrap(lambda n, r: gamma(n + 1) / gamma(n - r + 1))),
	'agm': (2, 2, func_wrap(agm)),
	'gcd': (2, 2, func_wrap(gcd)),
	'lcm': (2, 2, func_wrap(lcm)),
	'raw': (1, 1, func_radix(0)),
	'bin': (1, 1, func_radix(2)),
	'oct': (1, 1, func_radix(8)),
	'dec': (1, 1, func_radix(10)),
	'doz': (1, 1, func_radix(12)),
	'hex': (1, 1, func_radix(16)),
	'rad': (2, 2, lambda e, a: func_radix(a[1]['value'])(e, a)),
	'bc': (2, 2, lambda e, a: func_radix(a[1]['value'])(e, a)),
	'reverseBits': (2, 2, func_wrap(reversebits)),
	'reversebits': (2, 2, func_wrap(reversebits)),
	'reverseBytes': (2, 2, func_wrap(reversebytes)),
	'reversebytes': (2, 2, func_wrap(reversebytes)),
	'bitLength': (1, 1, func_wrap(bitlength)),
	'bitlength': (1, 1, func_wrap(bitlength)),
	'bitMingle': (2, 2, func_wrap(bitmingle)),
	'bitmingle': (2, 2, func_wrap(bitmingle)),
	'bitSelect': (2, 2, func_wrap(bitselect)),
	'bitselect': (2, 2, func_wrap(bitselect)),
	'bitand': (0, 0, func_reduce(lambda x, y: x & y, -1)),
	'bitor': (0, 0, func_reduce(lambda x, y: x | y, 0)),
	'bitxor': (0, 0, func_reduce(lambda x, y: x ^ y, 0)),
	'and': (0, 0, func_reduce(lambda x, y: x and y, True)),
	'or': (0, 0, func_reduce(lambda x, y: x or y, False)),
	'xor': (0, 0, func_reduce(lambda x, y: (not x) != (not y), False)),
	'equal': (0, 0, func_forallpairs(lambda x, y: x == y)),
	'asc': (0, 0, func_forallpairs(lambda x, y: x <= y)),
	'desc': (0, 0, func_forallpairs(lambda x, y: x >= y)),
	'inc': (0, 0, func_forallpairs(lambda x, y: x < y)),
	'incr': (0, 0, func_forallpairs(lambda x, y: x < y)),
	'decr': (0, 0, func_forallpairs(lambda x, y: x > y)),
	'ascending': (0, 0, func_forallpairs(lambda x, y: x <= y)),
	'descending': (0, 0, func_forallpairs(lambda x, y: x >= y)),
	'increasing': (0, 0, func_forallpairs(lambda x, y: x < y)),
	'decreasing': (0, 0, func_forallpairs(lambda x, y: x > y)),
	'if': (3, 3, func_wrap(lambda c, t, f: t if c else f)),
	'between': (3, 3, func_wrap(lambda a, b, c: a <= b <= c)),
	'minmax': (3, 3, func_wrap(median)),
	'median': (0, 0, func_wrap(median)),
	'all': (0, 0, func_iterwrap(all)),
	'any': (0, 0, func_iterwrap(any)),
	'bool': (1, 1, func_wrap(bool)),
	'float': (1, 1, func_wrap(float)),
	'copysign': (2, 2, func_wrap(math.copysign)),
	'fabs': (1, 1, func_wrap(math.fabs)),
	'fmod': (2, 2, func_wrap(math.fmod)),
	'fsum': (0, 0, func_iterwrap(math.fsum)),
}



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

def intfloatbase(s, b):
	if b == 0:
		try:
			return int(s)
		except:
			return float(s)
	if b < 2 or b > 36:
		raise ValueError('base must be >= 2 and <= 36')
	try:
		return int(s, b)
	except:
		return floatbase(s, b)



def strbase_digit(d):
	return chr(48 + d) if d < 10 else chr(55 + d)

def strbase_int(n, b):
	(d, m) = divmod(n, b)
	ms = strbase_digit(int(m))
	return strbase_int(d, b) + ms if d > 0 else ms

def strbase_frac(n, b):
	n *= b
	d = math.floor(n)
	n -= d
	ms = strbase_digit(int(d))
	return ms + strbase_frac(n, b) if n > 0 else ms

def strbase_prefix(b):
	if b == 0 or b == 10: return ''
	elif b == 2: return '0b'
	elif b == 8: return '0o'
	elif b == 12: return '0d'
	elif b == 16: return '0x'
	else: return str(b) + 'r'

def strbase(n, b, prefix=''):
	if b == 0:
		return str(n)
	elif b < 2 or b > 36:
		raise ValueError('base must be >= 2 and <= 36')
	elif math.isinf(n) or math.isnan(n):
		return str(n)
	elif n < 0:
		return '-' + strbase(-n, b, prefix)
	elif isinstance(n, (int, long)):
		return prefix + strbase_int(n, b)
	else:
		ip = math.floor(n)
		fp = n - ip
		ips = strbase_int(ip, b)
		fps = strbase_frac(fp, b)
		return prefix + ips + '.' + fps



def lex(s):
	i = 0
	n = len(s)
	while i < n:
		if ord(s[i]) <= 32:
			i += 1
			continue

		m = value_pattern.match(s, i, n)
		if m:
			r = {'type': 'value', 'image': m.group()}

			if m.group('bin'):
				r['radix'] = 2
				r['value'] = intfloatbase(m.group('binmag'), 2)
			elif m.group('oct'):
				r['radix'] = 8
				r['value'] = intfloatbase(m.group('octmag'), 8)
			elif m.group('doz'):
				r['radix'] = 12
				vs = m.group('dozmag')
				vs = re.sub('[AaTtXx]', 'A', vs)
				vs = re.sub('[BbEe]', 'B', vs)
				r['value'] = intfloatbase(vs, 12)
			elif m.group('hex'):
				r['radix'] = 16
				r['value'] = intfloatbase(m.group('hexmag'), 16)
			elif m.group('rad'):
				r['radix'] = int(m.group('radrad'))
				r['value'] = intfloatbase(m.group('radmag'), r['radix'])
			else:
				r['radix'] = 0
				r['value'] = intfloatbase(m.group('dec'), 0)

			if m.group('binexp'):
				r['value'] *= 2 ** int(m.group('binexpexp'))
			elif m.group('decexp'):
				r['value'] *= 10 ** int(m.group('decexpexp'))

			yield r
			i = m.end()
			continue

		m = id_pattern.match(s, i, n)
		if m:
			yield {'type': 'id', 'image': m.group()}
			i = m.end()
			continue

		for op in ops:
			if s.find(op, i, i + len(op)) == i:
				prec, image = ops_map[op]
				yield {'type': 'op', 'image': op, 'prec': prec, 'op': image}
				i += len(op)
				break
		else:
			raise ValueError('Unknown character in input starting at: ' + s[i:])



class parser:
	def __init__(self, input):
		self.tokens = list(lex(input))
		self.n = len(self.tokens)
		self.i = 0

	def parseFactor(self):
		if self.i >= self.n:
			raise ValueError('Expected value but found end of input')

		t = self.tokens[self.i]
		self.i += 1

		if t['type'] == 'value':
			return t

		if t['type'] == 'id':
			image = t['image']
			if image in consts:
				return {'type': 'value', 'image': image, 'value': consts[image], 'radix': 0}
			elif image in funcs:
				r = {'type': 'func', 'image': image, 'func': image, 'args': []}
				if self.i >= self.n:
					raise ValueError('Expected value but found end of input')
				elif self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['op'] == ':LP:':
					self.i += 1
					while True:
						r['args'].append(self.parseExpr())
						if self.i >= self.n:
							raise ValueError('Expected , or ) but found end of input')
						elif self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['op'] == ':RP:':
							self.i += 1
							return r
						elif self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['op'] == ':EOA:':
							self.i += 1
							continue
						else:
							raise ValueError('Expected , or ) but found ' + self.tokens[self.i]['image'])
				else:
					r['args'].append(self.parseFactor())
					return r
			else:
				return t

		if t['type'] == 'op':
			if t['op'] == ':LP:':
				r = self.parseExpr()
				if self.i >= self.n:
					raise ValueError('Expected ) but found end of input')
				elif self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['op'] == ':RP:':
					self.i += 1
					return r
				else:
					raise ValueError('Expected ) but found ' + self.tokens[self.i]['image'])
			if t['prec'] == 0 or t['prec'] == 3 or t['op'] == ':ROOT:':
				image = t['image']
				op = t['op']
				a = self.parseFactor();
				return {'type': 'unary', 'image': image, 'op': op, 'a': a}

		raise ValueError('Expected value but found ' + t['image'])

	def parseExpr(self, prec=13):
		a = self.parseFactor() if prec == 1 else self.parseExpr(prec - 1)
		while self.i < self.n and self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['prec'] == prec:
			image = self.tokens[self.i]['image']
			op = self.tokens[self.i]['op']
			self.i += 1
			b = self.parseExpr(prec) if (prec == 1 or prec == 13) else self.parseExpr(prec - 1)
			a = {'type': 'binary', 'image': image, 'op': op, 'a': a, 'b': b}
		return a

	def parse(self):
		r = [self.parseExpr()]
		while self.i < self.n and self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['op'] == ':EOS:':
			self.i += 1
			r.append(self.parseExpr())
		if self.i < self.n:
			raise ValueError('Expected end of input but found ' + self.tokens[self.i]['image'])
		return r



def bec_eval(bindings, e):
	if e['type'] == 'value':
		return e

	if e['type'] == 'id':
		image = e['image']
		if image in bindings:
			return bindings[image]
		else:
			raise ValueError('Undefined variable: ' + image)

	if e['type'] == 'func':
		args = [dict(bec_eval(bindings, a)) for a in e['args']]
		(minArgs, maxArgs, fn) = funcs[e['func']]
		if minArgs != 0 and len(args) < minArgs:
			raise ValueError('Too few arguments to function: ' + e['func'])
		if maxArgs != 0 and len(args) > maxArgs:
			raise ValueError('Too many arguments to function: ' + e['func'])
		return fn(e, args)

	if e['type'] == 'unary':
		a = dict(bec_eval(bindings, e['a']))
		if e['op'] == ':NOT:': a['value'] = not a['value']
		elif e['op'] == ':BITNOT:': a['value'] = ~a['value']
		elif e['op'] == ':ROOT:': a['value'] = math.sqrt(a['value'])
		elif e['op'] == ':CBRT:': a['value'] = math.pow(a['value'], 1.0/3.0)
		elif e['op'] == ':QTRT:': a['value'] = math.sqrt(math.sqrt(a['value']))
		elif e['op'] == ':ADD:': a['value'] = +a['value']
		elif e['op'] == ':SUB:': a['value'] = -a['value']
		else: raise ValueError('Undefined operator: ' + e['op'])
		return a

	if e['type'] == 'binary':
		b = dict(bec_eval(bindings, e['b']))
		if e['op'] == ':LET:':
			if e['a']['type'] == 'id':
				bindings[e['a']['image']] = b
				return b
			else:
				raise ValueError('Invalid lvalue: ' + e['a']['image'])

		a = dict(bec_eval(bindings, e['a']))
		if e['op'] == ':EXP:': a['value'] = a['value'] ** b['value']
		elif e['op'] == ':LOG:': a['value'] = math.log(a['value'], b['value'])
		elif e['op'] == ':ROOT:': a['value'] = math.pow(b['value'], 1.0/a['value'])
		elif e['op'] == ':MUL:': a['value'] = a['value'] * b['value']
		elif e['op'] == ':DIV:':
			if a['value'] % b['value'] == 0:
				a['value'] = a['value'] / b['value']
			else:
				a['value'] = float(a['value']) / float(b['value'])
		elif e['op'] == ':QUO:':
			r = a['value'] / b['value']
			if not isinstance(r, (int, long)):
				r = math.floor(r)
			a['value'] = r
		elif e['op'] == ':REM:':
			r = a['value'] / b['value']
			if not isinstance(r, (int, long)):
				r = math.floor(r)
			a['value'] = a['value'] - b['value'] * r
		elif e['op'] == ':ADD:': a['value'] = a['value'] + b['value']
		elif e['op'] == ':SUB:': a['value'] = a['value'] - b['value']
		elif e['op'] == ':LSH:': a['value'] = a['value'] << b['value']
		elif e['op'] == ':RSH:': a['value'] = a['value'] >> b['value']
		elif e['op'] == ':BITAND:': a['value'] = a['value'] & b['value']
		elif e['op'] == ':BITXOR:': a['value'] = a['value'] ^ b['value']
		elif e['op'] == ':BITOR:': a['value'] = a['value'] | b['value']
		elif e['op'] == ':LT:': a['value'] = a['value'] < b['value']
		elif e['op'] == ':GT:': a['value'] = a['value'] > b['value']
		elif e['op'] == ':LE:': a['value'] = a['value'] <= b['value']
		elif e['op'] == ':GE:': a['value'] = a['value'] >= b['value']
		elif e['op'] == ':EQ:': a['value'] = a['value'] == b['value']
		elif e['op'] == ':NE:': a['value'] = a['value'] != b['value']
		elif e['op'] == ':CMP:':
			if a['value'] == b['value']:
				a['value'] = 0
			elif a['value'] > b['value']:
				a['value'] = 1
			elif a['value'] < b['value']:
				a['value'] = -1
			else:
				a['value'] = float('nan')
		elif e['op'] == ':AND:': a['value'] = a['value'] and b['value']
		elif e['op'] == ':XOR:': a['value'] = (not a['value']) != (not b['value'])
		elif e['op'] == ':OR:': a['value'] = a['value'] or b['value']
		else: raise ValueError('Undefined operator: ' + e['op'])
		return a

def bec(bindings, s):
	for stat in parser(s).parse():
		r = bec_eval(bindings, stat)
		if stat['type'] != 'binary' or stat['op'] != ':LET:':
			yield strbase(r['value'], r['radix'], strbase_prefix(r['radix']))



def bec_print(bindings, s):
	try:
		for r in bec(bindings, s):
			print(r)
	except Exception as e:
		print(e)

def bec_repl(bindings):
	while True:
		sys.stdout.write('bec> ');
		try:
			line = sys.stdin.readline().strip()
			if line == 'bye' or line == 'exit' or line == 'quit':
				return
			elif line:
				bec_print(bindings, line)
		except:
			return

def bec_help(section):
	if section == 'operators':
		print('Operators:')
		print('    !     ¬           :N            boolean negation')
		print('    ~                       :n      bitwise negation')
		print('    √                 :V    :v      square root')
		print('    ∛                 :C    :c      cube root')
		print('    ∜                 :Q    :q      quartic root')
		print('    **    ^     ↑     :E    :e      exponentiation')
		print('    _     ↓           :G    :g      logarithm')
		print('    √                 :V    :v      root extraction')
		print('    *     ×     ·     :M    :m      multiplication')
		print('    /     ÷                         division')
		print('    \\                 :/            integer division')
		print('    %                               modulus / remainder')
		print('    +                               addition')
		print('    -                               subtraction')
		print('    <<    <<<   :[[   :L    :l      bitwise shift left')
		print('    >>    >>>   :]]   :R    :r      bitwise shift right')
		print('    &                       :a      bitwise and')
		print('    #                       :x      bitwise xor')
		print('    |                       :o      bitwise or')
		print('    <                 :[            less than')
		print('    >                 :]            greater than')
		print('    <=    =<    ≤     :[=   :=[     less than or equal to')
		print('    >=    =>    ≥     :]=   :=]     greater than or equal to')
		print('    =     ==    ===                 equal to')
		print('    <>    !=    !==   :[]           not equal to')
		print('    ≠     ≠≠    ≠≠≠   :/=   :=/     not equal to')
		print('    <=>   ⇔           :[=]          comparison')
		print('    &&                :A            boolean and')
		print('    ##                :X            boolean xor')
		print('    ||                :O            boolean or')
		print('    ←     :     :=    :==           assignment')
		print('    (     )     [     ]             parentheses')
		print('    ,                               argument separator')
		print('    ;                 ::            statement separator')
	elif section == 'constants':
		print('Constants:')
		ids = consts.keys()
		ids.sort()
		for id in ids:
			print('    %s    = %s' % ((id + '          ')[0:10], str(consts[id])))
	elif section == 'functions':
		print('Functions:')
		ids = funcs.keys()
		ids.sort()
		for i in range(0, len(ids)):
			if i % 4 == 0:
				sys.stdout.write('    ')
			sys.stdout.write((ids[i] + '                ')[0:16])
			if i % 4 == 3 or i == len(ids) - 1:
				sys.stdout.write('\n')
	else:
		print('')
		print('bec - Beckie\'s Extensive Calculator')
		print('')
		print('    bec -e <expr>       evaluate expressions in argument')
		print('    bec -f <path>       evaluate expressions in file')
		print('    bec -i              interactive mode')
		print('    bec -s              evaluate expressions from standard input')
		print('    bec <expr>          evaluate expressions in all arguments')
		print('')
		print('For more information:')
		print('')
		print('    bec --help constants')
		print('    bec --help operators')
		print('    bec --help functions')
		print('')

def bec_main(bindings, args):
	n = len(args)
	if n == 0:
		bec_help('')
		return
	i = 0
	while i < n:
		arg = args[i]
		i += 1
		if arg == '--help':
			if i < n:
				bec_help(args[i])
				i += 1
			else:
				bec_help('')
		elif arg == '-e':
			if i < n:
				bec_print(bindings, args[i])
				i += 1
		elif arg == '-f':
			if i < n:
				with open(args[i], 'r') as f:
					for line in f:
						line = line.strip()
						if line:
							bec_print(bindings, line)
				i += 1
		elif arg == '-i':
			bec_repl(bindings)
		elif arg == '-s':
			for line in sys.stdin:
				line = line.strip()
				if line:
					bec_print(bindings, line)
		else:
			line = ' '.join(args[i-1:]).strip()
			bec_print(bindings, line)
			return

if __name__ == '__main__':
	bec_main({}, sys.argv[1:])
