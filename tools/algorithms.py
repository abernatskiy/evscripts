def chunks(l, n):
	'''Yield successive n-sized chunks from l.'''
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def sumOfDicts(a, b):
	outDict = {}
	outDict.update(a)
	outDict.update(b)
	return outDict
