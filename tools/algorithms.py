def chunks(l, n):
	'''Yield successive n-sized chunks from l'''
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def sumOfDicts(a, b):
	'''Returns a dictionary which contais all keys and values from both input dictionaries'''
	outDict = {}
	outDict.update(a)
	outDict.update(b)
	return outDict

def listsIntersect(a, b):
	'''True iff there is at least one element in common between the two (iterable) arguments'''
	return any(i in a for i in b)
