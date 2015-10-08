import subprocess
import imp

import routes

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
       name is the name of the experiment
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
		self.queue = queue
		self.expectedWallClockTime = expectedWallClockTime

	def run(self):
		self._prepareEnv()
		self._submitJobs(0, self._numJobs()-1)
		self._waitForCompletion()
		self._processResults()

	def _prepareEnv(self):
		self._prepareDir()
		noteFile = open('notes.txt', 'w')
		noteFile.write('Experiment ' + self.name + ' initiated at ' + self._dateTime() + '\n')
		noteFile.close()

	def _prepareDir(self):
#		try:
		subprocess.call([sysEnv.mkdir, self.name])

	def _dateTime(self):
		return subprocess.check_output([sysEnv.date])[:-1]

	def _numJobs(self):
		if self.grid is None:
			return 1
		else:
			return (len(self.grid)+self.pointsPerJob-1) / self.pointsPerJob

	def _submitJobs(self, beginID, endID):
		pass

	def _waitForCompletion(self):
		pass

	def _processResults(self):
		pass
