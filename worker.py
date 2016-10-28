#!/usr/bin/python2

import sys
import os
from time import sleep
from copy import copy
import imp
from abc import ABCMeta, abstractmethod

def _getTimeString(tsecs):
	m, s = divmod(tsecs, 60)
	h, m = divmod(m, 60)
	return '%d:%02d:%02d' % (h, m, s)

class Worker(object):
	'''Abstract base class for Worker objects which handle execution of
     final experiment processes at cluster nodes.

     Abstract methods:
       runGroup(self, fullConditions) - function which executes the
         processes at exactly one set of experimental parameter values.
	'''
	__metaclass__ = ABCMeta
	def __init__(self, argv):
		'''This class is supposed to be constructed from sys.argv
       Arguments:
         argv[0] - script name (ignored)
         argv[1] - path to the evscripts directory
         argv[2] - job ID
         argv[3] - parent script
		'''
		self.evscriptsHome = argv[1]

		sys.path.append(self.evscriptsHome)
		self.routes = imp.load_source('routes', os.path.join(self.evscriptsHome, 'routes.py'))
		self.parentScript = imp.load_source('parent', os.path.join(self.evscriptsHome, argv[3]))
		self.translators = imp.load_source('translators', os.path.join(self.evscriptsHome, 'shared', 'translators.py')) # for filesystem names ONLY

		experiment = self.parentScript.initializeExperiment()

		jobID = int(argv[2])
		self.repeat, self.gridPoints, self.experimentalConditions = self._getConditions(experiment, jobID)
		self.rootDir = os.getcwd()

	def __repr__(self):
		return( 'Helper: evscriptsHome = ' + str(self.evscriptsHome) + '\n' +
						'        gridPoints = ' + str(self.gridPoints) + '\n' +
						'        experimentalConditions = ' + str(self.experimentalConditions) + '\n' +
						'        rootDir = ' + self.rootDir + '\n' +
						'        repeat = ' + str(self.repeat) + '\n')

	def __str__(self):
		return repr(self)

	def _getConditions(self, experiment, jobID):
		grid = experiment.grid
		expConds = experiment.experimentalConditions
		if grid is None:
			return (jobID, [{}], expConds)
		else:
			ppj = experiment.pointsPerJob
			gridLen = len(grid)
			jobsPerGrid = (gridLen + ppj - 1) / ppj
			curGridPointID = (jobID % jobsPerGrid)*ppj
			gridPoints = []
			for i in xrange(ppj):
				if curGridPointID+i < gridLen:
					gridPoints.append(grid[curGridPointID + i])
			return (jobID/jobsPerGrid, gridPoints, expConds)

	def runExperiments(self):
		for gridPoint in self.gridPoints:
			gpDirName = self.translators.dictionary2FilesystemName(gridPoint)
			if not os.path.isdir(gpDirName):
				os.makedirs(gpDirName)
			os.chdir(gpDirName)

			for condition in self.experimentalConditions:
				condDirName = self.translators.dictionary2FilesystemName(condition)
				if not os.path.isdir(condDirName):
					os.makedirs(condDirName)
				os.chdir(condDirName)

				fullCond = copy(condition)
				fullCond.update(gridPoint)

				self._makeGroupNote('Parameters of the run conducted here: ' + str(fullCond))
				et = os.times()[4]

				self.runGroup(fullCond)

				et = os.times()[4] - et
				self._makeGroupNote('Run completed in ' + str(et) + ' seconds (' + _getTimeString(et) + ' hours)')
				os.chdir('..')

			os.chdir('..')

	@abstractmethod
	def runGroup(self, fcond):
		pass

	def _makeGroupNote(self, str):
		f = open('groupNotes.txt', 'a')
		f.write(str + '\n')
		f.close()
