#!/usr/bin/env python
#coding=utf8

import re
import sys

try:
	from functools import reduce
except ImportError:
	pass



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

	'NOF': (0, 'pos'),
	'Nof': (0, 'pos'),
	'nof': (0, 'pos'),
	'POS': (0, 'pos'),
	'Pos': (0, 'pos'),
	'pos': (0, 'pos'),

	'IST': (0, 'nec'),
	'Ist': (0, 'nec'),
	'ist': (0, 'nec'),
	'NEC': (0, 'nec'),
	'Nec': (0, 'nec'),
	'nec': (0, 'nec'),

	'UNK': (0, 'con'),
	'Unk': (0, 'con'),
	'unk': (0, 'con'),
	'CON': (0, 'con'),
	'Con': (0, 'con'),
	'con': (0, 'con'),

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
	'IMPK': (4, 'imp'),
	'Impk': (4, 'imp'),
	'impk': (4, 'imp'),
	'IMPL': (4, 'impl'),
	'Impl': (4, 'impl'),
	'impl': (4, 'impl'),

	'-/>': (4, 'nimp'),
	'=/>': (4, 'nimp'),
	'↛': (4, 'nimp'),
	'⇏': (4, 'nimp'),
	'⊅': (4, 'nimp'),
	'NIMP': (4, 'nimp'),
	'Nimp': (4, 'nimp'),
	'nimp': (4, 'nimp'),
	'NIMPK': (4, 'nimp'),
	'Nimpk': (4, 'nimp'),
	'nimpk': (4, 'nimp'),
	'NIMPL': (4, 'nimpl'),
	'Nimpl': (4, 'nimpl'),
	'nimpl': (4, 'nimpl'),

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

ops = sorted(ops_map.keys())
ops.sort(key=len, reverse=True)



consts = {
	'NONE': None,
	'None': None,
	'none': None,
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



def ttstr(v):
	if v is None: return '-'
	if v is False: return '0'
	if v is True: return '1'
	return str(v)

def column_address(i):
	a = chr(65 + (i % 26))
	i //= 26
	while i:
		i -= 1
		a = chr(65 + (i % 26)) + a
		i //= 26
	return a

def parse_inputs(s):
	inputs = [x.strip() for x in s.split(',')]
	for i in range(len(inputs)):
		if not inputs[i]:
			inputs[i] = column_address(i)
	return inputs

def parse_outputs(s):
	def po_val(v):
		if v in '1HTYhty⊤': return True
		if v in '0FLNfln⊥': return False
		return None
	return [po_val(x) for x in s if x in '-01FHLNTUWXYZfhlntuwxyz⊤⊥']

def parse_minMax(e):
	groups = [x.strip() for x in e['args'].split(';') if x.strip()]

	if len(groups) == 1:
		try:
			terms = [int(x.strip()) for x in groups[0].split(',')]
			count = len(bin(max(abs(x) for x in terms))) - 2
			inputs = [column_address(i) for i in range(count)]
			e['inputs'], e['aterms'], e['bterms'] = inputs, terms, []
			e['args'] = ', '.join(str(x) for x in terms)
			return e
		except:
			raise ValueError('Illegal argument to function ' + e['func'])

	if len(groups) == 2:
		try:
			aterms = [int(x.strip()) for x in groups[0].split(',')]
			bterms = [int(x.strip()) for x in groups[1].split(',')]
			count = len(bin(max(abs(x) for x in aterms + bterms))) - 2
			inputs = [column_address(i) for i in range(count)]
			e['inputs'], e['aterms'], e['bterms'] = inputs, aterms, bterms
			e['args'] = '; '.join(', '.join(str(x) for x in y) for y in (aterms, bterms))
			return e
		except:
			pass
		try:
			inputs = parse_inputs(groups[0])
			terms = [int(x.strip()) for x in groups[1].split(',')]
			e['inputs'], e['aterms'], e['bterms'] = inputs, terms, []
			e['args'] = '; '.join(', '.join(str(x) for x in y) for y in (inputs, terms))
			return e
		except:
			raise ValueError('Illegal argument to function ' + e['func'])

	if len(groups) == 3:
		try:
			inputs = parse_inputs(groups[0])
			aterms = [int(x.strip()) for x in groups[1].split(',')]
			bterms = [int(x.strip()) for x in groups[2].split(',')]
			e['inputs'], e['aterms'], e['bterms'] = inputs, aterms, bterms
			e['args'] = '; '.join(', '.join(str(x) for x in y) for y in (inputs, aterms, bterms))
			return e
		except:
			raise ValueError('Illegal argument to function ' + e['func'])

	raise ValueError('Function ' + e['func'] + ' requires 1, 2, or 3 arguments, ' + str(len(groups)) + ' given')

def eval_minTerms(e, inputValues):
	index = int(''.join('1' if x else '0' for x in inputValues), 2)
	if index in e['aterms']: return True
	if index in e['bterms']: return None
	return False

def eval_maxTerms(e, inputValues):
	index = int(''.join('1' if x else '0' for x in inputValues), 2)
	if index in e['aterms']: return False
	if index in e['bterms']: return None
	return True

def eval_minMax(e, inputValues):
	index = int(''.join('1' if x else '0' for x in inputValues), 2)
	if index in e['aterms']: return True
	if index in e['bterms']: return False
	return None

def parse_valuesfn(e):
	groups = [x.strip() for x in e['args'].split(';') if x.strip()]

	if len(groups) == 1:
		values = parse_outputs(groups[0])
		count = len(bin(abs(len(values) - 1))) - 2
		inputs = [column_address(i) for i in range(count)]
		e['inputs'], e['values'] = inputs, values
		e['args'] = ''.join(ttstr(x) for x in values)
		return e

	if len(groups) == 2:
		inputs = parse_inputs(groups[0])
		values = parse_outputs(groups[1])
		e['inputs'], e['values'] = inputs, values
		e['args'] = ', '.join(inputs) + '; ' + ''.join(ttstr(x) for x in values)
		return e

	raise ValueError('Function ' + e['func'] + ' requires 1 or 2 arguments, ' + str(len(groups)) + ' given')

def eval_valuesfn(e, inputValues):
	index = int(''.join('1' if x else '0' for x in inputValues), 2)
	if index < len(e['values']): return e['values'][index]
	return None

funcs = {
	'minterms': (parse_minMax, eval_minTerms),
	'minTerms': (parse_minMax, eval_minTerms),
	'maxterms': (parse_minMax, eval_maxTerms),
	'maxTerms': (parse_minMax, eval_maxTerms),
	'minmax': (parse_minMax, eval_minMax),
	'minMax': (parse_minMax, eval_minMax),
	'values': (parse_valuesfn, eval_valuesfn),
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
			elif image in funcs:
				i = m.end()
				while i < n and ord(s[i]) <= 32:
					i += 1
				if i >= n:
					raise ValueError('Expected ( but found end of input')
				if s[i] not in '([':
					raise ValueError('Expected ( but found ' + s[i])
				i += 1
				j = i
				while j < n and s[j] not in '()[]':
					j += 1
				if j >= n:
					raise ValueError('Expected ) but found end of input')
				if s[j] not in ')]':
					raise ValueError('Expected ) but found ' + s[j])
				args = s[i:j].strip()
				yield {'type': 'func', 'image': image, 'func': image, 'args': args}
				j += 1
				i = j
				continue
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

		if t['type'] == 'func':
			return funcs[t['func']][0](t)

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
			return (ttstr(e['value']), 0)

		if e['type'] == 'id':
			return (e['image'], 0)

		if e['type'] == 'func':
			return (e['func'].lower() + '(' + e['args'] + ')', 0)

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

	if e['type'] == 'func':
		for image in e['inputs']:
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



def tvl_buf(v):
	if v is True: return True
	if v is False: return False
	return None

def tvl_not(v):
	if v is True: return False
	if v is False: return True
	return None

def tvl_and(u, v):
	if u is False or v is False: return False
	if u is True and v is True: return True
	return None

def tvl_nand(u, v):
	if u is False or v is False: return True
	if u is True and v is True: return False
	return None

def tvl_or(u, v):
	if u is True or v is True: return True
	if u is False and v is False: return False
	return None

def tvl_nor(u, v):
	if u is True or v is True: return False
	if u is False and v is False: return True
	return None

def tvl_xor(u, v):
	if u is False: return tvl_buf(v)
	if u is True: return tvl_not(v)
	return None

def tvl_xnor(u, v):
	if u is False: return tvl_not(v)
	if u is True: return tvl_buf(v)
	return None

def tvl_imp(u, v):
	if u is False or v is True: return True
	if u is True and v is False: return False
	return None

def tvl_nimp(u, v):
	if u is False or v is True: return False
	if u is True and v is False: return True
	return None

def tvl_impl(u, v):
	if u is False or v is True: return True
	if u is True and v is False: return False
	if u is True or v is False: return None
	return True

def tvl_nimpl(u, v):
	if u is False or v is True: return False
	if u is True and v is False: return True
	if u is True or v is False: return None
	return False

def tvl_pos(v):
	return v is not False

def tvl_nec(v):
	return v is True

def tvl_con(v):
	return not (v is True or v is False)

def tt_eval(bindings, e):
	if e['type'] == 'value':
		return e['value']

	if e['type'] == 'id':
		image = e['image']
		if image in bindings:
			return bindings[image]
		else:
			raise ValueError('Undefined variable: ' + image)

	if e['type'] == 'func':
		inputValues = []
		for image in e['inputs']:
			if image in bindings:
				inputValues.append(bindings[image])
			else:
				raise ValueError('Undefined variable: ' + image)
		return funcs[e['func']][1](e, inputValues)

	if e['type'] == 'unary':
		a = tt_eval(bindings, e['a'])
		if e['op'] == 'not': return tvl_not(a)
		if e['op'] == 'buf': return tvl_buf(a)
		if e['op'] == 'pos': return tvl_pos(a)
		if e['op'] == 'nec': return tvl_nec(a)
		if e['op'] == 'con': return tvl_con(a)
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
		if e['op'] == 'and': return tvl_and(a, b)
		if e['op'] == 'nand': return tvl_nand(a, b)
		if e['op'] == 'xor': return tvl_xor(a, b)
		if e['op'] == 'xnor': return tvl_xnor(a, b)
		if e['op'] == 'or': return tvl_or(a, b)
		if e['op'] == 'nor': return tvl_nor(a, b)
		if e['op'] == 'imp': return tvl_imp(a, b)
		if e['op'] == 'nimp': return tvl_nimp(a, b)
		if e['op'] == 'impl': return tvl_impl(a, b)
		if e['op'] == 'nimpl': return tvl_nimpl(a, b)
		if e['op'] == 'eq': return a is b
		if e['op'] == 'ne': return a is not b
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



def tt_simplify(inputs, minTerms, dontCares):
	def termTuples(inputs, minTerms, dontCares):
		for term in set(minTerms).union(set(dontCares)):
			m = (term,)
			s = bin(term)[2:].rjust(len(inputs), '0')
			yield (m, s)

	def strdiffs(a, b):
		for i in range(max(len(a), len(b))):
			if a[i] != b[i]:
				yield i

	def implicants(terms):
		for i in range(len(terms)):
			found = False
			for j in range(len(terms)):
				if i != j:
					d = list(strdiffs(terms[i][1], terms[j][1]))
					if len(d) == 1:
						m = tuple(sorted( set(terms[i][0]).union(set(terms[j][0])) ))
						s = terms[i][1][:d[0]] + '-' + terms[j][1][d[0]+1:]
						yield (m, s)
						found = True
			if not found:
				yield terms[i]

	def multiplySOP(sop0, sop1):
		# Applies the equivalence XX = X by yielding sets.
		# sop0, sop1 : Iterable<Iterable<T>>
		# p0, p1 : Iterable<T>
		# yields : Set<T>
		# returns : Generator<Set<T>>
		def multiplySOP2(sop0, sop1):
			for p0 in sop0:
				for p1 in sop1:
					yield set(p0).union(set(p1))
		# Applies the equivalence X + XY = X by discarding supersets.
		# sop0, sop1 : Iterable<Iterable<T>>
		# multiplySOP2() : Generator<Set<T>>
		# sorted(multiplySOP2()) : List<Set<T>>
		# newTerm, oldTerm : Set<T>
		# terms : List<Set<T>>
		terms = []
		for newTerm in sorted(multiplySOP2(sop0, sop1), key=len):
			for oldTerm in terms:
				if oldTerm.issubset(newTerm):
					break
			else:
				terms.append(newTerm)
		# Applies the equivalence X + X = X by returning a set.
		# terms : List<Set<T>>
		# t : Set<T>
		# returns : Set<Tuple<T>>
		return set(tuple(sorted(t)) for t in terms)

	def posToSOP(pos):
		# pos : Iterable<Iterable<T>>
		# terms : Iterable<T>
		# term : T
		# (term,) : Tuple<T>
		# set((term,)) : Set<Tuple<T>>
		# sops : List<Set<Tuple<T>>>
		# multiplySOP() : Set<Tuple<T>>
		# returns : Set<Tuple<T>>
		sops = [set((term,) for term in terms) for terms in pos]
		return reduce(multiplySOP, sops) if sops else ()

	def valuesToExprs(inputs, values):
		for i in range(len(values)):
			if values[i] == '0':
				yield '~' + inputs[i]
			if values[i] == '1':
				yield inputs[i]

	def productsToExprs(inputs, sop):
		for values in sorted([p[1] for p in sop], reverse=True):
			yield ' & '.join(valuesToExprs(inputs, values))

	def sopToExpr(inputs, sop):
		return ' | '.join(productsToExprs(inputs, sop))

	# Degenerate case of never true
	if not minTerms:
		yield '0'
		return

	# Find prime implicants
	imps = list(set(termTuples(inputs, minTerms, dontCares)))
	while True:
		tmp = set(implicants(imps))
		if tmp == set(imps): break
		imps = list(tmp)

	# Degenerate case of never false
	if len(imps) == 1 and imps[0][1].replace('-','') == '':
		yield '1'
		return

	# Find essential prime implicants
	epis = []
	rmt = []
	for term in minTerms:
		tmp = [imp for imp in imps if term in imp[0]]
		if len(tmp) == 1:
			epis.append(tmp[0])
			rmt.extend(tmp[0][0])

	# Build product of sums from reduced set of prime implicants
	pos = []
	for term in minTerms:
		if term not in rmt:
			tmp = [imp for imp in imps if term in imp[0]]
			pos.append(tmp)

	# If no prime implicants remaining, return the simplified expression
	if not pos:
		yield sopToExpr(inputs, sorted(set(epis)))
		return

	# Transform to sum of products
	sop = posToSOP(pos)
	# Choose products with fewest terms
	fewest = min(len(p) for p in sop)
	sop = [p for p in sop if len(p) == fewest]
	# Choose products with fewest inputs
	fewest = min(sum(f[1].count('0') + f[1].count('1') for f in p) for p in sop)
	sop = [p for p in sop if sum(f[1].count('0') + f[1].count('1') for f in p) == fewest]

	# Yield simplified expressions
	for p in sorted(sop, key=lambda sop: sorted([p[1] for p in sop], reverse=True), reverse=True):
		yield sopToExpr(inputs, set(epis).union(set(p)))



def tt_print(table):
	def tt_chk(expr, inputs, minTerms, maxTerms, dontCares, valuesByOutput):
		s, p, f = 0, 0, 0
		isHeader = True
		for iv, ov, ev in tt(';'.join(inputs) + ';' + expr):
			if isHeader:
				isHeader = False
			else:
				index = int(''.join('1' if x else '0' for x in iv), 2)
				if valuesByOutput[index] is None: s += 1
				elif valuesByOutput[index] is ev[len(inputs)]: p += 1
				else: f += 1
		return s == len(dontCares) and p == len(minTerms) + len(maxTerms) and f == 0

	try:
		isHeader = True
		inputs, outputs, exprs = [], [], []
		minTerms, maxTerms, dontCares = {}, {}, {}
		valuesByOutput = {}

		for inputValues, outputValues, exprValues in table:
			if isHeader:
				isHeader = False
				inputs = inputValues
				outputs = outputValues
				exprs = exprValues
				for k in outputs + exprs:
					minTerms[k] = set()
					maxTerms[k] = set()
					dontCares[k] = set()
					valuesByOutput[k] = {}
			elif inputs:
				index = int(''.join('1' if x else '0' for x in inputValues), 2)
				for i in range(len(outputValues)):
					valuesByOutput[outputs[i]][index] = outputValues[i]
					if outputValues[i] is None: dontCares[outputs[i]].add(index)
					if outputValues[i] is False: maxTerms[outputs[i]].add(index)
					if outputValues[i] is True: minTerms[outputs[i]].add(index)
				for i in range(len(exprValues)):
					valuesByOutput[exprs[i]][index] = exprValues[i]
					if exprValues[i] is None: dontCares[exprs[i]].add(index)
					if exprValues[i] is False: maxTerms[exprs[i]].add(index)
					if exprValues[i] is True: minTerms[exprs[i]].add(index)
			instr = '\t'.join(ttstr(x) for x in inputValues)
			outstr = '\t'.join(ttstr(x) for x in outputValues)
			exprstr = '\t'.join(ttstr(x) for x in exprValues)
			print('\t|\t'.join(x for x in (instr, outstr, exprstr) if x))

		if inputs:
			for k in outputs + exprs:
				print('')
				print('Output:\t' + k)
				print('Values:\t' + ''.join(ttstr(valuesByOutput[k][i]) for i in sorted(valuesByOutput[k])))
				print('Minterms:\t' + (', '.join(str(i) for i in sorted(minTerms[k])) if minTerms[k] else '-'))
				print('Maxterms:\t' + (', '.join(str(i) for i in sorted(maxTerms[k])) if maxTerms[k] else '-'))
				print('Don\'t Care:\t' + (', '.join(str(i) for i in sorted(dontCares[k])) if dontCares[k] else '-'))
				print('Simplified Forms:')
				for expr in tt_simplify(inputs, minTerms[k], dontCares[k]):
					# Verify that the simplified expression actually has the
					# same truth table, not counting "don't care" values
					assert tt_chk(expr, inputs, minTerms[k], maxTerms[k], dontCares[k], valuesByOutput[k]), 'Assertion failed!'
					print(expr)

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
				tt_print(tt(s))
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
	print('Alternate expression forms:')
	print('')
	print('    minterms(1, 2)             - function on A, B... with minterms 1, 2...')
	print('    minterms(1, 2; 3, 4)       - same but with "don\'t care" terms 3, 4...')
	print('    minterms(X, Y; 1, 2)       - function on X, Y... with minterms 1, 2...')
	print('    minterms(X, Y; 1, 2; 3, 4) - same but with "don\'t care" terms 3, 4...')
	print('                                 (unspecified terms will be maxterms)')
	print('    maxterms(1, 2)             - function on A, B... with maxterms 1, 2...')
	print('    maxterms(1, 2; 3, 4)       - same but with "don\'t care" terms 3, 4...')
	print('    maxterms(X, Y; 1, 2)       - function on X, Y... with maxterms 1, 2...')
	print('    maxterms(X, Y; 1, 2; 3, 4) - same but with "don\'t care" terms 3, 4...')
	print('                                 (unspecified terms will be minterms)')
	print('    minmax(1, 2; 3, 4)         - ...with minterms 1, 2... AND maxterms 3, 4...')
	print('    minmax(X, Y; 1, 2; 3, 4)   - ...with minterms 1, 2... AND maxterms 3, 4...')
	print('                                 (unspecified terms will be "don\'t care")')
	print('    values(1010--01)           - function on A, B... with truth table 1, 0...')
	print('    values(X, Y; 1010--01)     - function on X, Y... with truth table 1, 0...')
	print('                                 (false to true order; - or X is "don\'t care")')
	print('')

def tt_main(args):
	n = len(args)
	if n == 0:
		tt_help()
		return

	first = True
	i = 0
	while i < n:
		arg = args[i]
		i += 1
		if arg == '--help':
			tt_help()
		elif arg == '--test':
			for line in [
				'a and b; a or b; a xor b',
				'a & ~a & b & ~b',
				'a | ~a | b | ~b',
				'values(0000); values(0-0-); values(-0-0)',
				'values(0101); values(1010)',
				'values(-1-1); values(1-1-); values(1111)',
				'minterms(4,8,10,11,12,15;9,14)',
				'minterms(0,1,2,5,6,7)',
				'U:values(0001010111110110)',
				'V:values(0101110001010001)',
				'W:values(0001010100001001)',
				'X:values(0010010100110101)',
				'Y:values(0101001101010111)',
				'nof a; pos a; ist a; nec a; unk a; con a',
				'a imp b; a impk b; a impl b',
				'true and false; true or false; true; false',
			]:
				if not first: print('')
				tt_print(tt(line))
				first = False
		elif arg == '-e':
			if i < n:
				if not first: print('')
				tt_print(tt(args[i]))
				first = False
				i += 1
		elif arg == '-f':
			if i < n:
				with open(args[i], 'r') as f:
					for line in f:
						line = line.strip()
						if line:
							if not first: print('')
							tt_print(tt(line))
							first = False
				i += 1
		elif arg == '-i':
			tt_repl()
		elif arg == '-s':
			for line in sys.stdin:
				line = line.strip()
				if line:
					if not first: print('')
					tt_print(tt(line))
					first = False
		else:
			line = ' '.join(args[i-1:]).strip()
			if not first: print('')
			tt_print(tt(line))
			first = False
			return

if __name__ == '__main__':
	tt_main(sys.argv[1:])
