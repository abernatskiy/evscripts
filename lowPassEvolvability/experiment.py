import os
import sys
import shutil
import subprocess
import imp
from time import sleep

import routes
import shared.translators

sysEnv = imp.load_source('sysEnv', routes.sysEnv)
pbsEnv = imp.load_source('pbsEnv', routes.pbsEnv)

class Experiment(object):
	'''Base class for Experiment objects.
     These objects are intended for use in computational
     experiments in evolutionary computation ran on
     PBS-based supercomputers.
	'''
	def __init__(self, name, experimentalConditions, grid=None, pointsPerJob=1, queue=None, expectedWallClockTime=None):
		'''Arguments:
       name is the name of the experiment AND of its
         working directory.
       experimentalConditions is a list of dictionaries
         describing parameters for different experimental
         groups. The number of experimental groups is
         equal to the length of the list. In each
         dictionary the keys are the names of experimental
         parameters and the values are their values.
       grid is an object desribing the set of extra
         (e.g. environmental) conditions under which we
         wish to know the experiment's outcome. Must be
         iterable and yield parameter dictionaries of the
         same type as the ones used in
         experimentalConditions. The default is to
         conduct the experiment just once under no extra
         conditions.
       pointsPerJob indicates how many experiments
         should be conducted per cluster job. The default
         is one, and that includes performing runs for
         all parameter sets in experimentalConditions.
       queue is the name of the queue which is to be used
         for the jobs. Default is read from the PBS
         database (see exampleRoutes.py).
       expectedWallClockTime is a PBS-parsable string
         desribing a time span of a single job. Examples:
           03:00:00 - three hours
           7:00:00:00 - seven days
         Cutoff time of the queue is used by default.
		'''
		self.name = name
		self.experimentalConditions = experimentalConditions
		self.grid = grid
		self.pointsPerJob = pointsPerJob
		self.queue = pbsEnv.defaultQueue if queue is None else queue
		self.expectedWallClockTime = pbsEnv.queueLims[self.queue] if expectedWallClockTime is None else expectedWallClockTime

	def run(self):
		self._prepareEnv()
		self._submitJobs(0, self._numJobs()-1)
		self._waitForCompletion()
		self._processResults()

	def _prepareEnv(self):
		self._makeDir()
		os.chdir(self.name)
		self._makeNote('Experiment ' + self.name + ' initiated at ' + self._dateTime())

	def _makeNote(self, line):
		noteFile = open('experimentNotes.txt', 'a')
		noteFile.write(line + '\n')
		noteFile.close()

	def _makeDir(self):
		'''Creates a working directory named after the experiment in the current directory'''
		if os.path.isdir(self.name):
			print('Working directory exists, trying to back it up and create a new one...')
			for i in xrange(10):
				curCandidateDir = self.name + '.save' + str(i)
				if not os.path.isdir(curCandidateDir):
					break
				else:
					curCandidateDir = None
			if curCandidateDir is None:
				raise OSError('Too many backup directories (no less than ten). Go clean them up.')
			else:
				shutil.move(self.name, curCandidateDir)
		elif os.path.exists(self.name):
			raise OSError('Working directory path exists, but is not a directory. Go fix it.')
		os.makedirs(self.name)

	def _dateTime(self):
		return subprocess.check_output([sysEnv.date])[:-1]

	def _numJobs(self):
		if self.grid is None:
			return 1
		else:
			return (len(self.grid)+self.pointsPerJob-1) / self.pointsPerJob

	def _submitJobs(self, beginID, endID):
		cmdList = [pbsEnv.qsub,
			'-q', self.queue,
			'-l',  'walltime=' + self.expectedWallClockTime,
			'-t', str(beginID) + '-' + str(endID),
			'-v', 'PYTHON=' + sys.executable +
           ',PYTHON_HELPER=' + str(routes.pbsPythonHelper) +
           ',EVSCRIPTS_HOME=' + routes.evscriptsHome +
           ',CONDITIONS=' + self._getConditionsString() +
           ',GRID=' + self._getGridString() +
           ',POINTS_PER_JOB=' + str(self.pointsPerJob),
			routes.pbsBashHelper]
		self._makeNote('qsub cmdline: ' + subprocess.list2cmdline(cmdList))
		subprocess.check_call(cmdList)

	def _getGridString(self):
		if self.grid is None:
			return 'None'
		else:
			return self.grid.toCompactString()

	def _getConditionsString(self):
		return shared.translators.listOfDictionaries2CompactString(self.experimentalConditions)

	def _waitForCompletion(self):
		while subprocess.check_output([pbsEnv.qstat, '-u', 'abernats']) != '':
			sleep(120)

	def _processResults(self):
		pass
