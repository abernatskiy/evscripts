#!/usr/bin/python2

import sys
import os
from time import sleep
from copy import copy
import imp
from abc import ABCMeta, abstractmethod

class Helper(object):
	'''Abstract base class for Helper objects which handle execution of
     the final experiment processes at cluster nodes.

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
		self.gridPoints = self._getGridPoints(experiment.grid, experiment.pointsPerJob, jobID)
		self.experimentalConditions = experiment.experimentalConditions
		self.rootDir = os.getcwd()

	def __repr__(self):
		return( 'Helper: evscriptsHome = ' + str(self.evscriptsHome) + '\n' +
						'        gridPoints = ' + str(self.gridPoints) + '\n' +
						'        experimentalConditions = ' + str(self.experimentalConditions) + '\n' +
						'        rootDir = ' + self.rootDir + '\n' )

	def __str__(self):
		return repr(self)

	def _getGridPoints(self, grid, pointsPerJob, jobID):
		gridPoints = []
		if grid is None:
			gridPoints.append({})
		else:
			curGridPointID = jobID*pointsPerJob
			for i in xrange(pointsPerJob):
				if curGridPointID+i < len(grid):
					gridPoints.append(grid[curGridPointID + i])
		return gridPoints

	def runExperiments(self):
		for gridPoint in self.gridPoints:
			gpDirName = self.translators.dictionary2FilesystemName(gridPoint)
			os.makedirs(gpDirName)
			os.chdir(gpDirName)

			for condition in self.experimentalConditions:
				condDirName = self.translators.dictionary2FilesystemName(condition)
				os.makedirs(condDirName)
				os.chdir(condDirName)

				fullCond = copy(condition)
				fullCond.update(gridPoint)
				self.runGroup(fullCond)

				os.chdir('..')

			os.chdir('..')

	@abstractmethod
	def runGroup(self, fcond):
		self._makeGroupNote('Parameters of the run conducted here: ' + str(fcond))

	def _makeGroupNote(self, str):
		f = open('groupNotes.txt', 'a')
		f.write(str + '\n')
		f.close()
