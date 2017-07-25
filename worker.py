#!/usr/bin/python2

import sys
import os
from time import sleep,time
from copy import copy
import imp
import subprocess

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
		self.pbsGridWalker = routes.pbsGridWalker
		self.parentScript = imp.load_source('parent', argv[1])
		self.runComputationAtPoint = self.parentScript.runComputationAtPoint
		self.pointsPerJob = int(argv[2])
		self.rootDir = os.getcwd()
		self.dbname = os.path.abspath('experiment.db')

	def __repr__(self):
		return( 'Worker: pbsGridWalker = ' + str(self.pbsGridWalker) + '\n' +
						'        parentScript = ' + str(self.parentScript) + '\n' +
						'        rootDir = ' + self.rootDir + '\n' +
						'        pointsPerJob = ' + str(self.pointsPerJob) + '\n')

	def __str__(self):
		return repr(self)

	def spawnProcess(self, cmdList):
		self.makeGroupNote('Spawning a process with command ' + subprocess.list2cmdline(cmdList) + ' at ' + os.getcwd())
		return subprocess.Popen(cmdList)

	def killProcess(self, process, label='unknown'):
		self.makeGroupNote('Killing a process (pid {}, label {})'.format(process.pid, label))
		process.send_signal(subprocess.signal.SIGTERM)

	def runCommand(self, cmdList):
		command = subprocess.list2cmdline(cmdList)
		self.makeGroupNote('Running command ' + command + ' at ' + os.getcwd())
		try:
			subprocess.check_call(cmdList)
			return True
		except subprocess.CalledProcessError:
			self.makeGroupNote('Command ' + command + ' failed')
			return False

	def makeGroupNote(self, str):
		print(str)
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

				self.makeGroupNote('Grid parameters of the run conducted here: ' + str(params))
				elapsedTime = time()
				if self.runComputationAtPoint(self, params):
					gridSql.reportSuccessOnPoint(self.dbname, id)
				else:
					gridSql.reportFailureOnPoint(self.dbname, id)
				elapsedTime = time() - elapsedTime
				self.makeGroupNote('Run completed in ' + str(elapsedTime) + ' seconds (' + _getTimeString(elapsedTime) + ' hours) of wall clock time')

				os.chdir('..')

				self.pointsPerJob -= 1
			else:
				print('WORKER: No points left in the grid, finishing walking the grid before the allowed number of points per job has been reached.')
				return
		print('WORKER: Hit the allowed number of points per job, finishing walking the grid.')

if __name__ == '__main__':
	w = Worker(sys.argv)
	w.runAtAllPoints()
