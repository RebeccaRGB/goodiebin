#!/usr/bin/env python
#coding=utf8

import re
import sys



id_pattern = re.compile('⊥|⊤|[A-Za-z0-9]+')



ops_map = {
	'!': (0, 'not'),
	'-': (0, 'not'),
	'/': (0, 'not'),
	'~': (0, 'not'),
	'¬': (0, 'not'),
	'¯': (0, 'not'),
	'NOT': (0, 'not'),
	'Not': (0, 'not'),
	'not': (0, 'not'),

	'_': (0, 'buf'),
	'¡': (0, 'buf'),
	'⌐': (0, 'buf'),
	'⌙': (0, 'buf'),
	'BUF': (0, 'buf'),
	'Buf': (0, 'buf'),
	'buf': (0, 'buf'),
	'BOOL': (0, 'buf'),
	'Bool': (0, 'buf'),
	'bool': (0, 'buf'),
	'BOOLEAN': (0, 'buf'),
	'Boolean': (0, 'buf'),
	'boolean': (0, 'buf'),

	'&': (1, 'and'),
	'&&': (1, 'and'),
	'&&&': (1, 'and'),
	'*': (1, 'and'),
	'.': (1, 'and'),
	'·': (1, 'and'),
	'×': (1, 'and'),
	'∧': (1, 'and'),
	'/\\': (1, 'and'),
	'AND': (1, 'and'),
	'And': (1, 'and'),
	'and': (1, 'and'),

	'!&': (1, 'nand'),
	'-&': (1, 'nand'),
	'/&': (1, 'nand'),
	'~&': (1, 'nand'),
	'¬&': (1, 'nand'),
	'¯&': (1, 'nand'),
	'↑': (1, 'nand'),
	'⊼': (1, 'nand'),
	'/|\\': (1, 'nand'),
	'NAND': (1, 'nand'),
	'Nand': (1, 'nand'),
	'nand': (1, 'nand'),

	'^': (2, 'xor'),
	'^^': (2, 'xor'),
	'^^^': (2, 'xor'),
	'#': (2, 'xor'),
	'##': (2, 'xor'),
	'###': (2, 'xor'),
	'⊕': (2, 'xor'),
	'⊻': (2, 'xor'),
	'XOR': (2, 'xor'),
	'Xor': (2, 'xor'),
	'xor': (2, 'xor'),

	'!^': (2, 'xnor'),
	'-^': (2, 'xnor'),
	'/^': (2, 'xnor'),
	'~^': (2, 'xnor'),
	'¬^': (2, 'xnor'),
	'¯^': (2, 'xnor'),
	'!#': (2, 'xnor'),
	'-#': (2, 'xnor'),
	'/#': (2, 'xnor'),
	'~#': (2, 'xnor'),
	'¬#': (2, 'xnor'),
	'¯#': (2, 'xnor'),
	'⊙': (2, 'xnor'),
	'NXOR': (2, 'xnor'),
	'Nxor': (2, 'xnor'),
	'nxor': (2, 'xnor'),
	'XNOR': (2, 'xnor'),
	'Xnor': (2, 'xnor'),
	'xnor': (2, 'xnor'),

	'|': (3, 'or'),
	'||': (3, 'or'),
	'|||': (3, 'or'),
	'+': (3, 'or'),
	'∥': (3, 'or'),
	'∨': (3, 'or'),
	'\\/': (3, 'or'),
	'OR': (3, 'or'),
	'Or': (3, 'or'),
	'or': (3, 'or'),

	'!|': (3, 'nor'),
	'-|': (3, 'nor'),
	'/|': (3, 'nor'),
	'~|': (3, 'nor'),
	'¬|': (3, 'nor'),
	'¯|': (3, 'nor'),
	'↓': (3, 'nor'),
	'⊽': (3, 'nor'),
	'\\|/': (3, 'nor'),
	'NOR': (3, 'nor'),
	'Nor': (3, 'nor'),
	'nor': (3, 'nor'),

	'->': (4, 'imp'),
	'=>': (4, 'imp'),
	'→': (4, 'imp'),
	'⇒': (4, 'imp'),
	'⊃': (4, 'imp'),
	'IMP': (4, 'imp'),
	'Imp': (4, 'imp'),
	'imp': (4, 'imp'),

	'-/>': (4, 'nimp'),
	'=/>': (4, 'nimp'),
	'↛': (4, 'nimp'),
	'⇏': (4, 'nimp'),
	'⊅': (4, 'nimp'),
	'NIMP': (4, 'nimp'),
	'Nimp': (4, 'nimp'),
	'nimp': (4, 'nimp'),

	'=': (5, 'eq'),
	'==': (5, 'eq'),
	'===': (5, 'eq'),
	'<->': (5, 'eq'),
	'<=>': (5, 'eq'),
	'↔': (5, 'eq'),
	'⇔': (5, 'eq'),
	'≡': (5, 'eq'),
	'EQ': (5, 'eq'),
	'Eq': (5, 'eq'),
	'eq': (5, 'eq'),

	'!=': (5, 'ne'),
	'!==': (5, 'ne'),
	'<>': (5, 'ne'),
	'</>': (5, 'ne'),
	'≠': (5, 'ne'),
	'≠≠': (5, 'ne'),
	'≠≠≠': (5, 'ne'),
	'↮': (5, 'ne'),
	'⇎': (5, 'ne'),
	'≢': (5, 'ne'),
	'NE': (5, 'ne'),
	'Ne': (5, 'ne'),
	'ne': (5, 'ne'),

	':': (6, ':='),
	':=': (6, ':='),
	':==': (6, ':='),
	'<-': (6, ':='),
	'<=': (6, ':='),
	'←': (6, ':='),
	'⇐': (6, ':='),

	'(': (7, ':LP:'),
	')': (7, ':RP:'),
	'[': (7, ':LP:'),
	']': (7, ':RP:'),
	',': (8, ':EOS:'),
	';': (8, ':EOS:'),
	'::': (8, ':EOS:'),
}

ops = ops_map.keys()
ops.sort()
ops.sort(key=len, reverse=True)



consts = {
	'0': False,
	'⊥': False,
	'FALSE': False,
	'False': False,
	'false': False,
	'1': True,
	'⊤': True,
	'TRUE': True,
	'True': True,
	'true': True,
}



def lex(s):
	i = 0
	n = len(s)
	while i < n:
		if ord(s[i]) <= 32:
			i += 1
			continue

		m = id_pattern.match(s, i, n)
		if m:
			image = m.group()
			if image in consts:
				yield {'type': 'value', 'image': image, 'value': consts[image]}
			elif image in ops:
				prec, opname = ops_map[image]
				yield {'type': 'op', 'image': image, 'prec': prec, 'op': opname}
			else:
				yield {'type': 'id', 'image': image}
			i = m.end()
			continue

		for op in ops:
			if s.find(op, i, i + len(op)) == i:
				prec, opname = ops_map[op]
				yield {'type': 'op', 'image': op, 'prec': prec, 'op': opname}
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
			if t['prec'] == 0:
				image = t['image']
				opname = t['op']
				a = self.parseFactor();
				return {'type': 'unary', 'image': image, 'prec': 0, 'op': opname, 'a': a}

		raise ValueError('Expected value but found ' + t['image'])

	def parseExpr(self, prec=6):
		if prec == 1:
			a = self.parseFactor()
		else:
			a = self.parseExpr(prec - 1)
		while self.i < self.n and self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['prec'] == prec:
			image = self.tokens[self.i]['image']
			opname = self.tokens[self.i]['op']
			self.i += 1
			if prec == 1:
				b = self.parseFactor()
			elif prec == 6:
				b = self.parseExpr(prec)
			else:
				b = self.parseExpr(prec - 1)
			a = {'type': 'binary', 'image': image, 'prec': prec, 'op': opname, 'a': a, 'b': b}
		return a

	def parse(self):
		r = [self.parseExpr()]
		while self.i < self.n and self.tokens[self.i]['type'] == 'op' and self.tokens[self.i]['op'] == ':EOS:':
			self.i += 1
			r.append(self.parseExpr())
		if self.i < self.n:
			raise ValueError('Expected end of input but found ' + self.tokens[self.i]['image'])
		return r



def tt_toString(e):
	def tt_toString2(e):
		if e['type'] == 'value':
			return (('1' if e['value'] else '0'), 0)

		if e['type'] == 'id':
			return (e['image'], 0)

		if e['type'] == 'unary':
			a, prec = tt_toString2(e['a'])
			if prec > e['prec']:
				a = '(' + a + ')'
			return (e['op'] + ' ' + a, e['prec'])

		if e['type'] == 'binary':
			a, prec = tt_toString2(e['a'])
			if prec > e['prec']:
				a = '(' + a + ')'
			b, prec = tt_toString2(e['b'])
			if prec > e['prec']:
				b = '(' + b + ')'
			return (a + ' ' + e['op'] + ' ' + b, e['prec'])

	s, _ = tt_toString2(e)
	return s



def tt_inputs_outputs(e, inputs=None, outputs=None):
	if e['type'] == 'value':
		return (inputs, outputs)

	if e['type'] == 'id':
		image = e['image']
		if outputs is None or image not in outputs:
			if inputs is None:
				inputs = {image}
			else:
				inputs.add(image)
		return (inputs, outputs)

	if e['type'] == 'unary':
		return tt_inputs_outputs(e['a'], inputs, outputs)

	if e['type'] == 'binary':
		if e['op'] == ':=':
			if e['a']['type'] == 'id':
				image = e['a']['image']
				inputs, outputs = tt_inputs_outputs(e['b'], inputs, outputs)
				if inputs is not None and image in inputs:
					raise ValueError('Late-defined variable: ' + tt_toString(e['a']))
				if outputs is not None and image in outputs:
					raise ValueError('Redefined variable: ' + tt_toString(e['a']))
				if outputs is None:
					outputs = {image}
				else:
					outputs.add(image)
				return (inputs, outputs)
			else:
				raise ValueError('Invalid lvalue: ' + tt_toString(e['a']))
		inputs, outputs = tt_inputs_outputs(e['a'], inputs, outputs)
		inputs, outputs = tt_inputs_outputs(e['b'], inputs, outputs)
		return (inputs, outputs)



def tt_eval(bindings, e):
	if e['type'] == 'value':
		return e['value']

	if e['type'] == 'id':
		image = e['image']
		if image in bindings:
			return bindings[image]
		else:
			raise ValueError('Undefined variable: ' + image)

	if e['type'] == 'unary':
		a = tt_eval(bindings, e['a'])
		if e['op'] == 'not': return not a
		if e['op'] == 'buf': return not not a
		raise ValueError('Undefined operator: ' + e['op'])

	if e['type'] == 'binary':
		if e['op'] == ':=':
			if e['a']['type'] == 'id':
				image = e['a']['image']
				b = tt_eval(bindings, e['b'])
				bindings[image] = b
				return b
			else:
				raise ValueError('Invalid lvalue: ' + tt_toString(e['a']))
		a = tt_eval(bindings, e['a'])
		b = tt_eval(bindings, e['b'])
		if e['op'] == 'and': return a and b
		if e['op'] == 'nand': return not (a and b)
		if e['op'] == 'xor': return (not a) != (not b)
		if e['op'] == 'xnor': return (not a) == (not b)
		if e['op'] == 'or': return a or b
		if e['op'] == 'nor': return not (a or b)
		if e['op'] == 'imp': return b or not a
		if e['op'] == 'nimp': return a and not b
		if e['op'] == 'eq': return (not a) == (not b)
		if e['op'] == 'ne': return (not a) != (not b)
		raise ValueError('Undefined operator: ' + e['op'])



def tt(s):
	stats = list(parser(s).parse())
	inputs = set()
	outputs = set()
	exprs = []

	for stat in stats:
		inputs, outputs = tt_inputs_outputs(stat, inputs, outputs)
		if stat['type'] != 'binary' or stat['op'] != ':=':
			exprs.append(tt_toString(stat))

	inputs = sorted(list(inputs))
	outputs = sorted(list(outputs))
	yield (inputs, outputs, exprs)

	def tt_helper(inputValues):
		if len(inputValues) >= len(inputs):
			bindings = {}
			exprValues = []
			for i in range(len(inputs)):
				bindings[inputs[i]] = inputValues[i]
			for stat in stats:
				r = tt_eval(bindings, stat)
				if stat['type'] != 'binary' or stat['op'] != ':=':
					exprValues.append(r)
			outputValues = [bindings[o] for o in outputs]
			yield (inputValues, outputValues, exprValues)
		else:
			for row in tt_helper(inputValues + [False]):
				yield row
			for row in tt_helper(inputValues + [True]):
				yield row

	for row in tt_helper([]):
		yield row



def tt_print(s):
	def ttstr(v):
		if v is False: return '0'
		if v is True: return '1'
		return str(v)

	try:
		for inputs, outputs, exprs in tt(s):
			inputs = '\t'.join(ttstr(x) for x in inputs)
			outputs = '\t'.join(ttstr(x) for x in outputs)
			exprs = '\t'.join(ttstr(x) for x in exprs)
			print('\t|\t'.join(x for x in (inputs, outputs, exprs) if x))
	except Exception as e:
		print(e)

def tt_repl():
	while True:
		sys.stdout.write('tt> ')
		try:
			s = sys.stdin.readline().strip()
			if s == 'bye' or s == 'exit' or s == 'quit':
				return
			elif s:
				tt_print(s)
		except:
			return

def tt_help():
	print('')
	print('truthtable - print truth tables of boolean expressions')
	print('')
	print('    truthtable -e <expr>    evaluate expressions in argument')
	print('    truthtable -f <path>    evaluate expressions in file')
	print('    truthtable -i           interactive mode')
	print('    truthtable -s           evaluate expressions from standard input')
	print('    truthtable <expr>       evaluate expressions in all arguments')
	print('')
	print('Accepted operators:')
	print('')
	print('    False:          0  ⊥  FALSE  False  false')
	print('    True:           1  ⊤  TRUE  True  true')
	print('    AND:            &  &&  &&&  *  .  ·  ×  ∧  /\\  AND  And  and')
	print('    OR:             |  ||  |||  +  ∥  ∨  \\/  OR  Or  or')
	print('    XOR:            ^  ^^  ^^^  #  ##  ###  ⊕  ⊻  XOR  Xor  xor')
	print('    NOT:            !  -  /  ~  ¬  ¯  NOT  Not  not')
	print('    NAND:           !&  -&  /&  ~&  ¬&  ¯&  ↑  ⊼  /|\\  NAND  Nand  nand')
	print('    NOR:            !|  -|  /|  ~|  ¬|  ¯|  ↓  ⊽  \\|/  NOR  Nor  nor')
	print('    XNOR:           !^ -^ /^ ~^ ¬^ ¯^ !# -# /# ~# ¬# ¯# ⊙ XNOR Xnor xnor')
	print('    No-Op:          _  ¡  ⌐  ⌙  BUF  Buf  buf  BOOL  Bool  bool')
	print('    Implies:        ->  =>  →  ⇒  ⊃  IMP  Imp  imp')
	print('    Not Implies:    -/>  =/>  ↛  ⇏  ⊅  NIMP  Nimp  nimp')
	print('    Equals:         =  ==  ===  <->  <=>  ↔  ⇔  ≡  EQ  Eq  eq')
	print('    Not Equals:     !=  !==  <>  </>  ≠  ≠≠  ≠≠≠  ↮  ⇎  ≢  NE  Ne  ne')
	print('    Assignment:     :  :=  :==  <-  <=  ←  ⇐')
	print('    Parentheses:    (  )  [  ]')
	print('    Delimiter:      ,  ;  ::')
	print('')

def tt_main(args):
	n = len(args)
	if n == 0:
		tt_help()
		return
	i = 0
	while i < n:
		arg = args[i]
		i += 1
		if arg == '--help':
			tt_help()
		elif arg == '-e':
			if i < n:
				tt_print(args[i])
				i += 1
		elif arg == '-f':
			if i < n:
				with open(args[i], 'r') as f:
					for line in f:
						line = line.strip()
						if line:
							tt_print(line)
				i += 1
		elif arg == '-i':
			tt_repl()
		elif arg == '-s':
			for line in sys.stdin:
				line = line.strip()
				if line:
					tt_print(line)
		else:
			line = ' '.join(args[i-1:]).strip()
			tt_print(line)
			return

if __name__ == '__main__':
	tt_main(sys.argv[1:])