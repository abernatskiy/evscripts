'''Shared tools for coding and decoding of some data structures to and from strings'''

# Compact string format

import itertools

_separators = ['_', ':'] # First element of the list is the top level separator

def _nestedIterable2CompactString(nestedIterable):
	'''The bottom level iterator must yield strings'''
	def _iterable2CompactString(iterable):
		return _separators[1].join(iterable)
	return _separators[0].join(map(_iterable2CompactString, nestedIterable))

def _compactString2NestedIterable(str):
	return map(lambda x: x.split(_separators[1]), str.split(_separators[0]))

def namedRanges2CompactString(nameRange, valRanges):
	if len(nameRange) != len(valRanges):
		raise ValueError('Parameter names and ranges lists are out of alignment')
	namedRanges = [ [nameRange[i]] + map(str, valRanges[i]) for i in xrange(len(nameRange)) ]
	return _nestedIterable2CompactString(namedRanges)

def compactString2NamedRanges(str):
	parsedStrings = _compactString2NestedIterable(str)
	paramsNames = []
	paramsRanges = []
	for namedRangeList in parsedStrings:
		paramsNames.append(namedRangeList[0])
		paramsRanges.append(list(map(float, namedRangeList[1:])))
	return (paramsNames, paramsRanges)

def listOfDictionaries2CompactString(dictList):
	def dict2StrList(dict):
		strLoL = [ [ item[0], str(item[1]) ] for item in dict.items() ]
		return itertools.chain(*strLoL)
	return _nestedIterable2CompactString(map(dict2StrList, dictList))

def compactString2ListOfDictionaries(str):
	parsedStrings = _compactString2NestedIterable(str)
	def dictFromStrList(list):
		keys = list[0::2]
		vals = map(float, list[1::2])
		return dict(zip(keys, vals))
	return list(map(dictFromStrList, parsedStrings))

# Strings for the filesystem

def dictionary2FilesystemName(dictionary):
	return '_'.join(map(lambda (x, y): x + str(y), dictionary.items()))
