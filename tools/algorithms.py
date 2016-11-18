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

def classifyDict(dict, classifier, safely=True):
	'''{a:1, b:2, c:3, d:4} + {I: [a,b], II: [c]} -> {I: {a:1, b:2}, II: {c:3}}
	   If safely flag is on, will throw ValueError if the first dictionary
	   has any keys unknown to the classifier
	'''
	classified = {}
	for category, catkeys in classifier.items():
		classified[category] = {}
		for catkey in catkeys:
			try:
				classified[category][catkey] = dict[catkey]
			except KeyError:
				if safely:
					raise ValueError('Cannot classify key {}. Check your dictionary!')
	return classified

def listsIntersect(a, b):
	'''True iff there is at least one element in common between the two (iterable) arguments'''
	return any(i in a for i in b)

def ratioCeil(numerator, denomenator):
	'''Returns ceiling of the ratio of numerator and denumenator'''
	return (numerator+denomenator-1) / denomenator
