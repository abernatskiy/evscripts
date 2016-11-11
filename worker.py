#!/usr/bin/python2

import sys
import os
from time import sleep
from copy import copy
import imp

import routes
import gridSql
import tools.fsutils as tfs

def _getTimeString(tsecs):
	m, s = divmod(tsecs, 60)
	h, m = divmod(m, 60)
	return '%d:%02d:%02d' % (h, m, s)

class Worker(object):
	'''Abstract base class for Worker objects which handle the execution
     of the experiment processes at cluster nodes.

     Will use the function runComputationAtPoint(worker, fullConditions)
	   from the parent script to execute the computation at exactly one
	   point in parametric space. The function can assume that it will be
	   executed from within the point's directory. It must return True iff
	   the computation was completed successfully.
	'''
	def __init__(self, argv):
		'''Should be constructed from sys.argv
       Fields:
         argv[0] - script name, ignored
         argv[1] - parent script
		     argv[2] - number of points the worker should attempt to process
		       within its life cycle
		'''
		self.evscriptsHome = routes.evscriptsHome
		self.parentScript = imp.load_source('parent', argv[1])
		self.runComputationAtPoint = self.parentScript.runComputationAtPoint
		self.pointsPerJob = int(argv[2])
		self.rootDir = os.getcwd()
		self.dbname = os.path.abspath('experiment.db')

	def __repr__(self):
		return( 'Worker: evscriptsHome = ' + str(self.evscriptsHome) + '\n' +
						'        parentScript = ' + str(self.parentScript) + '\n' +
						'        rootDir = ' + self.rootDir + '\n' +
						'        pointsPerJob = ' + str(self.pointsPerJob) + '\n')

	def __str__(self):
		return repr(self)

	def makeGroupNote(self, str):
		with open('groupNotes.txt', 'a') as f:
			f.write(str + '\n')

	def runAtAllPoints(self):
		while self.pointsPerJob > 0:
			pointTriple = gridSql.requestPointFromGridQueue(self.dbname)
			if pointTriple:
				id, curPass, params = pointTriple
				gpDirName = tfs.dictionary2filesystemName(params)
				tfs.makeDirCarefully(gpDirName)
				os.chdir(gpDirName)

				self.makeGroupNote('Parameters of the run conducted here: ' + str(params))
				elapsedTime = os.times()[4]
				if self.runComputationAtPoint(self, params):
					gridSql.reportSuccessOnPoint(self.dbname, id)
				else:
					gridSql.reportFailureOnPoint(self.dbname, id)
				elapsedTime = os.times()[3] - elapsedTime
				self.makeGroupNote('Run completed in ' + str(elapsedTime) + ' seconds (' + _getTimeString(elapsedTime) + ' hours)')

				os.chdir('..')

				self.pointsPerJob -= 1
			else:
				return

if __name__ == '__main__':
	w = Worker(sys.argv)
	w.runAtAllPoints()
