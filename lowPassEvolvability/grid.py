import itertools

class Grid(object):
	def __init__(self, paramsNames, paramsRanges):
		if len(paramsNames) == len(paramsRanges):
			self.dim = len(paramsNames)
		else:
			raise ValueError('Parameter names and ranges lists are out of alignment')
		self.paramsNames = paramsNames
		self.gridvals = list(itertools.product(*paramsRanges))

	def __repr__(self):
		return repr(list(self))

	def __len__(self):
		return len(self.gridvals)

	def __iter__(self):
		for gridvec in self.gridvals:
			yield {self.paramsNames[i]: gridvec[i] for i in xrange(self.dim)}

	def __getitem__(self, j):
		return {self.paramsNames[i]: self.gridvals[j][i] for i in xrange(self.dim)}

class RegularGrid(Grid):
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
				getVal = lambda i: referenceValue * modifier**i
			else:
				raise ValueError('Second field of the parameter grid description must be either \'lin\' or \'log\'')
			paramsRanges.append([ getVal(i) for i in xrange(downSteps, upSteps+1) ])
		super(RegularGrid, self).__init__(paramsNames, paramsRanges)
