'''Shared tools for coding and decoding of some data structures to and from strings'''

# Strings for the filesystem
def dictionary2FilesystemName(dictionary):
	return '_'.join(map(lambda (x, y): x + str(y), dictionary.items()))
