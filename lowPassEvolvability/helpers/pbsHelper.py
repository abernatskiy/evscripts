#!/usr/bin/python2

import sys
import os
from time import sleep
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

	def _getGridPoints(self, gridString, pointsPerJob, jobID):
		self.gridPoints = []
		if argv[4] != 'None':
			grid = imp.load_source('grid', os.path.join(self.evscriptsHome + 'grid.py'))
			globalGrid = grid.Grid([], [])
			globalGrid.fromCompactString(gridString)
			curGridPointID = jobID*pointsPerJob
			for i in xrange(pointsPerJob):
				self.gridPoints.append(globalGrid[curGridPointID + i])

	def _getConditionsFromString(self, conditionsString)
		dictStrings = map(lambda x: x.split(','), conditionsString.split(';'))
		def dictFromStrList(list):
			keys = list[0::2]
			vals = map(float, list[1::2])
			return dict(zip(keys, vals))
		self.experimentalConditions = list(map(dictFromStrList, dictStrings))

if __name__ == '__main__':
	os.makedirs('fgsfds')
	os.chdir('fgsfds')
	f = open('helpernotes.log', 'w')
	f.write('Arguments:' + str(sys.argv) + '\n')
	f.write('Attempting to create Helper...\n')
	f.flush()
	h = Helper(sys.argv)
	f.write('evscriptsHome = ' + str(h.evscriptsHome))
	f.flush()
	f.write('gridPoints = ' + str(h.gridPoints))
	f.flush()
	f.write('experimentalConditions = ' + str(h.experimentalConditions))
	f.close()
	print('DONE')
