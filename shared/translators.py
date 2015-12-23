'''Shared tools for coding and decoding of some data structures to and from strings'''

import numbers

# Strings for the filesystem
def dictionary2FilesystemName(dictionary):
	'''Turns a parameter dictionary into a filesystem-appropriate string,
     ignoring non-numeric values in the dictionary.
     Tip: boolean values are considered numeric.
	'''
	filteredDict = {k: v for k, v in dictionary.iteritems() if isinstance(v, numbers.Number)}
	if len(filteredDict) == 0:
		if len(dictionary) > 0:
			print('WARNING: Nontrivial numberless dictionary ' + str(dictionary) + ' gets converted into a default string (\'None\') - this may cause some filesystem names to not be unique')
		return 'None'
	else:
		return '_'.join(map(lambda (x, y): x + str(y), sorted(filteredDict.items())))
