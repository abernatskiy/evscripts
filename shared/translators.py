'''Shared tools for coding and decoding of some data structures to and from strings'''

import numbers

# Strings for the filesystem
def dictionary2FilesystemName(dictionary):
	'''Turns a parameter dictionary into a filesystem-appropriate string,
     ignoring non-numeric values in the dictionary.
     Tip: boolean values are considered numeric.
	'''
	filteredDict = {k: v for k, v in dictionary.iteritems() if isinstance(v, numbers.Number)}
	return '_'.join(map(lambda (x, y): x + str(y), filteredDict.items()))
