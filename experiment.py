import os
import sys
import shutil
import subprocess
import imp
from time import sleep
from abc import ABCMeta, abstractmethod

import routes
import gridSql
import tools.fsutils as tfs

sysEnv = imp.load_source('sysEnv', routes.sysEnv)
pbsEnv = imp.load_source('pbsEnv', routes.pbsEnv)

class Experiment(object):
	'''Abstract base class for Experiment classes, which are
	   supposed to help run computational experiments with
	   multiple parameters on PBS-based supercomputers.

	   User interface definitions (see helpstrings):
	     Experiment.__init__(self,
	       name,
	       experimentalConditions,
	       grid=None,
	       pointsPerJob=1,
	       queue=None,
	       expectedWallClockTime=None,
	       dryRun=False,
	       repeats=1
	     )
	     Experiment.run()

     Abstract methods:
       prepareEnv(self) - must create a suitable
         environment for the experiments.
         May include creating config files, compiling
         custom binaries, etc.
         Is executed at the work dir (./<name>).
       processResults(self) - processes the results.
         Is executed at the work dir (./<name>).

     Handy utilities for building processResults():
       executeAtEveryExperimentDir(self, function, cargs, kwargs)
       executeAtEveryConditionsDir(self, function, cargs, kwargs)
         - self-explanatory, works only within the work dir.
       enterWorkDir(self)
       exitWorkDir(self) - for user navigation when calling
         processResults() outside of run(),
         NOT NEEDED IN MOST CASES
	'''
	__metaclass__ = ABCMeta

	def __init__(self, name, grid, pointsPerJob=1, passes=1, queue=None, expectedWallClockTime=None, maxJobs=None, repos={}, dryRun=False):
		'''Arguments:
       name: the name of the experiment, its
         working directory and its main database
         (located at <name>/<name>.db).
       grid: describes the set of conditions under
         which we wish to see the computation's outcome.
         Must be iterable, indexable and yield parameter
         dictionaries with parameter names as keys and
         parameter values as values.
       pointsPerJob: indicates how many instances of
         computation should be performed within one
         cluster job. The default is one, meaning
         that each point of the parametric grid will be
         processed as a separate job. Useful for short
         jobs.
       passes: how many passes does your calculation
         require. Default is 1. Useful for very long
         computations with checkpointing.
       queue: the name of the queue which is to be used
         for the jobs. Default is specified on per-host
         basis in the defaultQueue variable at the host
         environment file (pointed to by pbsEnv variable
         at the routes.py).
       maxJobs: how many workers should the system spawn
         at any given moment. The default is
         ceil(len(grid)/pointPerJob), the maximum number of
         workers which can be ran concurrently without
         some of them waiting idle.
       expectedWallClockTime: a scheduler-parsable string
         desribing a time span of a single job. Examples:
           03:00:00 - three hours
           7:00:00:00 - seven days
         Cutoff time of the queue is used by default.
       repos: Experiment class automatically checks and
         stores info about versions and diffs of git
         repositories used in the computation. By default
         it will only monitor its own version; add all the
         other software it uses here. The format is:
           {'componentName': 'pathToComponentsRepo'}
         You will probably want to fix this variable in
         daughter classes.
			 dryRun: set to true to perform a dry run.
		'''
		self.name = name
		self._checkFSNameUniqueness(grid)
		self.grid = grid
		self.pointsPerJob = pointsPerJob
		self.passes = passes
		self.queue = queue if queue else pbsEnv.defaultQueue
		self.maxJobs = maxJobs if maxJobs else (len(grid)+self.pointsPerJob-1) / self.pointsPerJob
		self.expectedWallClockTime = expectedWallClockTime if expectedWallClockTime else pbsEnv.queueLims[self.queue]
		if passes != 1 and pointPerJob > 1:
			print('WARNING: You\'re trying to run a multistage job with more than one grid point per job. It is advisable to split computation into grid points as much as possible before splitting the points themselves')
		self.repos = repos
		self.dryRun = dryRun

		self._curJobIDs = []
		self.dbname = 'experiment.db'

	# Abstract methods: defining these defines an Experiment class

	@abstractmethod
	def prepareEnv(self):
		'''Must be executed by any child through super.
       The child may then assume that it operates inside the working dir.
    '''
		tfs.makeDirCarefully(self.name)
		self.enterWorkDir()
		self.makeNote('Experiment ' + self.name + ' initiated at ' + self._dateTime())
		self._recordVersions()
		self.makeNote('Apps versions recorded successfully')
		gridSql.makeGridTable(self.grid, self.dbname)
		gridSql.makeGridQueueTable(self.dbname, passes=self.passes)

	@abstractmethod
	def processResults(self):
		pass

	# Convenience functions - use these in definitions of the abstract methods

	def makeNote(self, line):
		with open('experimentNotes.txt', 'a') as noteFile:
			noteFile.write(line + '\n')

	# self.run() - classes' main method

	def run(self):
		self.prepareEnv()
		# farm workers
		jobsSubmitted = 0
		while not gridSql.checkForCompletion(self.dbname):
			self._weedWorkers()
			while len(self._curJobIDs) < self.maxJobs:
				self._spawnWorker()
				jobsSubmitted += 1
				sleep(pbsEnv.qsubDelay)
				if jobsSubmitted > self.maxJobs*self.passes:
					self.makeNote('Expected {} jobs, submitted {}: likely some workers failed'.format(self.maxJobs*self.passes, jobsSubmitted))
					if self.dryRun:
						break
			if self.dryRun:
				break
			sleep(pbsEnv.qstatCheckingPeriod)
		# finishing touches
		self.processResults()
		self.exitWorkDir() # entered it at prepareEnv()

	# Internals

	def enterWorkDir(self):
		if not os.path.isdir(self.name):
			raise OSError('Cannot find working dir ' + self.name)
		os.chdir(self.name)

	def exitWorkDir(self):
		os.chdir('..')

	def _checkFSNameUniqueness(self, iterable):
		dirNames = map(translator.dictionary2filesystemName, iterable)
		if not len(dirNames) == len(set(dirNames)):
			raise ValueError('Dirnames produces by the grid are not all unique:\n' + '\n'.join(dirNames))

	def _dateTime(self):
		return subprocess.check_output([sysEnv.date])[:-1]

	def _recordVersions(self):
		def pathVerRecord(file, repoName, repoPath):
			curDir = os.getcwd()
			os.chdir(repoPath)
			versionStr = subprocess.check_output([sysEnv.git, 'rev-parse', 'HEAD'])
			branchOut = subprocess.check_output([sysEnv.git, 'branch'])
			branchStr = filter(lambda str: str.find('* ') == 0, branchOut.split('\n'))[0].replace('* ', '')
			diffStr = subprocess.check_output([sysEnv.git, 'diff'])
			file.write(repoName + ' path: ' + repoPath + '\n' +
									repoName + ' branch: ' + branchStr + '\n' +
									repoName + ' version: ' + versionStr + '\n' +
									'git diff for ' + repoName + ':\n' + diffStr +'\n' +
									'-------------------------\n')
			os.chdir(curDir)
		with open('versions.txt', 'w') as verFile:
			pathVerRecord(verFile, 'evscripts', routes.evscriptsHome)
			for repoName in self.repos.keys():
				pathVerRecord(verFile, repoName, self.repos[repoName])

	def _spawnWorker(self):
		cmdList = [pbsEnv.qsub,
			'-q', self.queue,
			'-l',  'walltime=' + self.expectedWallClockTime,
			'-v', 'PYTHON=' + sys.executable +
						',EVSCRIPTS_HOME=' + routes.evscriptsHome +
						',PARENT_SCRIPT=' + os.path.abspath(sys.argv[0]) +
						',POINTS_PER_JOB=' + str(self.pointsPerJob),
			os.path.join(routes.evscriptsHome, 'pbs.sh')]
		self.makeNote('qsub cmdline: ' + subprocess.list2cmdline(cmdList))
		if not self.dryRun:
			curJobID = subprocess.check_output(cmdList)
			for t in xrange(3000):
				if curJobID in subprocess.check_output([pbsEnv.qstat, '-f', '-u', pbsEnv.user]):
					print('Job ' + self._curJobID + ' was successfully submitted')
					self._curJobIDs.append(curJobID)
					return
				sleep(0.2)
			raise RuntimeError('Failed to submit job: qsub worked, but the job did not apper in queue within 10 minutes')

	def _weedWorkers(self):
		cmdList = [pbsEnv.qstat, '-f', '-u', pbsEnv.user]
		if not self.dryRun:
			qstat = subprocess.check_output(cmdList)
			self._curJobIDs = [ jobID for jobID in self._curJobIDs if jobID in qstat ]
		else:
			self.makeNote('Dry run note: would execute ' + subprocess.list2cmdline(cmdList))

       #  def executeAtEveryExperimentDir(self, function, cargs, kwargs):
       #  	'''The function must accept a grid point parameter dictionary as its first argument'''
       #  	for gridPoint in self.grid:
       #  		gpDirName = shared.translators.dictionary2FilesystemName(gridPoint)
       #  		try:
       #  			os.chdir(gpDirName)
       #  			args = (gridPoint,) + cargs
       #  			function(*args, **kwargs)
       #  			os.chdir('..')
       #  		except OSError as err:
       #  			print('\033[93mWarning!\033[0m Could not enter directory \033[1m' + err.filename + '\033[0m')

       #  def executeAtEveryConditionsDir(self, condFunc, condCArgs, condKWArgs):
       #  	'''Function condFunc must accept a grid point parameter dictionary as its first
       # argument and a conditions parameter dictionary as its second argument.
       #  	'''
       #  	def executeAtEveryConditionsDir(gridPoint, expObj, function, cargs, kwargs):
       #  		for condPoint in expObj.experimentalConditions:
       #  			condDirName = shared.translators.dictionary2FilesystemName(condPoint)
       #  			try:
       #  				os.chdir(condDirName)
       #  				args = (gridPoint, condPoint) + cargs
       #  				function(*args, **kwargs)
       #  				os.chdir('..')
       #  			except OSError as err:
       #  				print('\033[93mWarning!\033[0m Could not enter directory \033[1m' + err.filename + '\033[0m')
       #  	condArgs = (self, condFunc, condCArgs, condKWArgs)
       #  	self.executeAtEveryExperimentDir(executeAtEveryConditionsDir, condArgs, {})

       #  def addResultRecord(self, resultsFileName, paramsDict, resultsDict):
       #  	'''Appends a record to a results accumulating file. Can be exeuted from
       # any point. File format:
       #   # paramsKey0 ... paramsKeyN resultsKey0 ... resultsKeyM
       #   paramsVal0 ... paramsValN resultsVal0 ... resultsValM
       # The header comment is only added when the function is called for the
       # first time, the result lines are only appended afterwards.
       # If the function is called with a different set of parameter/result
       # names than the one used in the intial call, ValueError is raised.
       # For best results, keep the keys short (under 20 symbols).'''
       #  	sortingFunction = sorted
       #  	numDecimals = 13
       #  	numReprWidth = numDecimals + 7
       #  	def writeRowOfKeys(file, keys, initialShift=0):
       #  		for name in keys:
       #  			adjStr = name.ljust(numReprWidth - initialShift, ' ')
       #  			file.write(' ' + adjStr)
       #  			initialShift = 0
       #  	def writeRowOfVals(file, keys, dict, leadingSpaces=1):
       #  		for name in keys:
       #  			valStr = ( '%.' + str(numDecimals) + 'e' ) % dict[name]
       #  			valStr = valStr.rjust(numReprWidth, ' ')
       #  			file.write(' '*leadingSpaces + valStr)
       #  			leadingSpaces = 1
       #  	with open(os.path.join(self._resultsDir, resultsFileName), 'a') as file:
       #  		if self._resultsFiles.has_key(resultsFileName):
       #  			origParamNames, origResultNames = self._resultsFiles[resultsFileName]
       #  			if set(paramsDict.keys()) != set(origParamNames) or set(resultsDict.keys()) != set(origResultNames):
       #  				print 'Reprs: orig param ' + repr(origParamsDict) + ' new param ' + repr(paramsDict) + ' orig results ' + repr(origResultsDict) + ' new results ' + repr(resultsDict) + '\n'
       #  				raise ValueError('Error: trying to write heterogenous data into ' + resultsFileName)
       #  		else:
       #  			origParamNames, origResultNames = sortingFunction(paramsDict.keys()), sortingFunction(resultsDict.keys())
       #  			self._resultsFiles[resultsFileName] = (origParamNames, origResultNames)
       #  			file.write('#')
       #  			writeRowOfKeys(file, origParamNames, initialShift=2)
       #  			writeRowOfKeys(file, origResultNames)
       #  			file.write('\n')
       #  		writeRowOfVals(file, origParamNames, paramsDict, leadingSpaces=0)
       #  		writeRowOfVals(file, origResultNames, resultsDict)
       #  		file.write('\n')
