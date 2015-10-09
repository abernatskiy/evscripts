#!/usr/bin/python2

import sys
import os
from time import sleep
from copy import copy
import imp

class Helper:
	def __init__(self, argv):
    #This class is supposed to be constructed from sys.argv
    #Arguments:
    #  argv[0] - script name (ignored)
    #  argv[1] - path to the evscripts directory
    #  argv[2] - job ID
    #  argv[3] - conditions string
    #  argv[4] - grid string
    #  argv[5] - number of points per job
		self.evscriptsHome = argv[1]
		self._getGridPoints(argv[4], int(argv[5]), int(argv[2]))
		self._getConditionsFromString(argv[3])
		self.rootDir = os.getcwd()

	def __repr__(self):
		return( 'Helper: evscriptsHome = ' + str(self.evscriptsHome) + '\n' +
						'        gridPoints = ' + str(self.gridPoints) + '\n' +
						'        experimentalConditions = ' + str(self.experimentalConditions) + '\n' +
						'        rootDir = ' + self.rootDir + '\n' )

	def __str__(self):
		return repr(self)

	def _getGridPoints(self, gridString, pointsPerJob, jobID):
		self.gridPoints = []
		if gridString == 'None':
			self.gridPoints.append({})
		else:
			grid = imp.load_source('grid', os.path.join(self.evscriptsHome + 'grid.py'))
			globalGrid = grid.Grid([], [])
			globalGrid.fromCompactString(gridString)
			curGridPointID = jobID*pointsPerJob
			for i in xrange(pointsPerJob):
				self.gridPoints.append(globalGrid[curGridPointID + i])

	def _getConditionsFromString(self, conditionsString):
		dictStrings = map(lambda x: x.split(':'), conditionsString.split('_'))
		def dictFromStrList(list):
			keys = list[0::2]
			vals = map(float, list[1::2])
			return dict(zip(keys, vals))
		self.experimentalConditions = list(map(dictFromStrList, dictStrings))

	def runExperiments(self):
		def dict2dirName(dict):
			return '_'.join(map(lambda (x, y): x + str(y), dictionary.items()))
		for gridPoint in self.gridPoints:
			gpDirName = dict2dirName(gridPoint)
			os.makedirs(gpDirName)
			os.chdir(gpDirName)

			for condition in self.experimentalConditions:
				condDirName = dict2dirName(condition)
				os.makedirs(condDirName)
				os.chdir(condDirName)

				fullCond = copy(condition)
				fullCond.update(gridPoint)
				self._runGroup(fullCond)

				os.chdir('..')

			os.chdir('..')

	def _runGroup(self, fcond):
		f = open('groupnotes.txt', 'w')
		f.write(str(fcond))
		f.close()

if __name__ == '__main__':
	f = open('helpernotes.txt', 'w')
	f.write('Arguments: ' + str(sys.argv) + '\n')
	f.write('Attempting to create Helper...\n')
	f.flush()
	h = Helper(sys.argv)
	f.write(str(h))
	f.close()
	h.runExperiments()
	print('DONE')
