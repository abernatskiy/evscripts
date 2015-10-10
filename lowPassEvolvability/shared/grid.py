import itertools

import translators

class Grid(object):
	'''Class which allows iteration over arbitrarily dimensional parameter grids.
     The set of grid points is defined to be a direct product of 1d grids for
     individual parameters. Iteration over an object of this class yields
     parameter disctionaries.
	'''
	def __init__(self, paramsNames, paramsRanges):
		'''Arguments:
         paramsNames - a list of the string names of the parameters
         paramsRanges - a list of iterables representing one-dimensional
          grids of individual parameters
    '''
		if len(paramsNames) == len(paramsRanges):
			self.dim = len(paramsNames)
		else:
			raise ValueError('Parameter names and ranges lists are out of alignment')
		self.paramsNames = paramsNames
		self.paramsRanges = list(map(lambda x: list(map(float, x)), paramsRanges)) # every value in rangers is forcibly converted to float
		self.gridvals = list(itertools.product(*self.paramsRanges))

	def __repr__(self):
		return repr(list(self))

	def __len__(self):
		return len(self.gridvals)

	def __iter__(self):
		for gridvec in self.gridvals:
			yield {self.paramsNames[i]: gridvec[i] for i in xrange(self.dim)}

	def __getitem__(self, j):
		item = {self.paramsNames[i]: self.gridvals[j][i] for i in xrange(self.dim)}
		item['randomSeed'] = 9001.0 #TODO fix random seed treatment
		return item

	def toCompactString(self):
		return translators.namedRanges2CompactString(self.paramsNames, self.paramsRanges)

	def fromCompactString(self, string):
		self.paramsNames, self.paramsRanges = compactString2NamedRanges(string)
		self.dim = len(self.paramsNames)
		self.gridvals = list(itertools.product(*self.paramsRanges))

class LogLinGrid(Grid):
	def __init__(self, paramsDescriptions):
		'''Descriptions must be an iterable yielding tuples of the following form:
         (paramName, gridType, referenceValue, modifier, downSteps, upSteps)
       where
         paramName is the name of the parameter
         gridType is a type of the grid for the parameter,
           can be 'lin' or 'log'
       The grid for this parameter is formed by taking
       downSteps decrements of the referenceValue followed
       by itself, followed by upSteps increments of it.
       Incrementing means adding modifier for 'lin'
       grids and multiplying by modifier for 'log'
       grids; decrementing means subtraction of and
       division by modifier, correspondingly.
    '''
		paramsNames = []
		paramsRanges = []
		for paramName, gridType, referenceValue, modifier, downSteps, upSteps in paramsDescriptions:
			paramsNames.append(paramName)
			if gridType == 'lin':
				getVal = lambda i: referenceValue + float(i)*modifier
			elif gridType == 'log':
				getVal = lambda i: referenceValue * (modifier**(i+1))
			else:
				raise ValueError('Second field of the parameter grid description must be either \'lin\' or \'log\'')
			print 'Paramname ' + paramName
			print 'Range ' + str([ getVal(i) for i in xrange(-1*downSteps, upSteps+1) ])
			paramsRanges.append([ getVal(i) for i in xrange(-1*downSteps, upSteps+1) ])
		super(LogLinGrid, self).__init__(paramsNames, paramsRanges)
