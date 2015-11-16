import os
import sys
import shutil
import subprocess
import imp
from time import sleep
from abc import ABCMeta, abstractmethod

import routes
import shared.translators

sysEnv = imp.load_source('sysEnv', routes.sysEnv)
pbsEnv = imp.load_source('pbsEnv', routes.pbsEnv)

class Experiment(object):
	'''Abstract base class for Experiment objects.
     These objects are intended for use in computational
     experiments in evolutionary computation ran on
     PBS-based supercomputers.

     Abstract methods:
       prepareEnv(self) - must create a suitable
         environment for the experiments.
         May include creating config files, compiling
         custom binaries, etc.
         Is executed at the work dir (./<name>).
       processResults(self) - processes the results.
         Is executed at the work dir (./<name>).

     Handy utilities for building processResults():
       enterWorkDir(self)
       exitWorkDir(self) - for user navigation when calling
         processResults() outside of run()
       executeAtEveryExperimentDir(self, function, cargs, kwargs)
       executeAtEveryConditionsDir(self, function, cargs, kwargs)
         - self-explanatory, works only within the work dir.
	'''
	__metaclass__ = ABCMeta

	def __init__(self, name, experimentalConditions, grid=None, pointsPerJob=1, queue=None, expectedWallClockTime=None, dryRun=False):
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
         conditions. Saved into the member variable
         self.grid.
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
			dryRun shows whether or not you want to perform
         time-consuming operations or just do a dry run.
         Available as self.dryRun.
		'''
		self.name = name
		self._checkFSNameUniqueness(experimentalConditions)
		self.experimentalConditions = experimentalConditions
		self._checkFSNameUniqueness(grid)
		self.grid = grid
		self.pointsPerJob = pointsPerJob
		self.queue = pbsEnv.defaultQueue if queue is None else queue
		self.expectedWallClockTime = pbsEnv.queueLims[self.queue] if expectedWallClockTime is None else expectedWallClockTime
		self._resultsDir = os.path.join(os.getcwd(), name, 'results')
		self._resultsFiles = {}
		self.dryRun = dryRun

	def _checkFSNameUniqueness(self, iterable):
		if iterable is not None:
			dirNames = map(shared.translators.dictionary2FilesystemName, iterable)
			if not len(dirNames) == len(set(dirNames)):
				raise ValueError('Dirnames produces by conditions are not unique:\n' + '\n'.join(dirNames))

	def run(self):
		self.prepareEnv()
		self._submitJobs(0, self._numJobs()-1)
		self._waitForCompletion()
		self.processResults()
		self.exitWorkDir() # entered it at prepareEnv()

	@abstractmethod
	def prepareEnv(self):
		'''Must be executed by any child through super.
       The child may assume that it operates inside the working dir.
    '''
		self._makeWorkDir()
		self.enterWorkDir()
		self._makeNote('Experiment ' + self.name + ' initiated at ' + self._dateTime())
		self._recordVersions()
		self._makeNote('Apps versions recorded successfully')
		os.makedirs(self._resultsDir)

	def _makeNote(self, line):
		noteFile = open('experimentNotes.txt', 'a')
		noteFile.write(line + '\n')
		noteFile.close()

	def _makeWorkDir(self):
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

	def enterWorkDir(self):
		if not os.path.isdir(self.name):
			raise OSError('Cannot find working dir ' + self.name)
		os.chdir(self.name)

	def exitWorkDir(self):
		os.chdir('..')

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
						',PARENT_SCRIPT=' + os.path.basename(sys.argv[0]),
			routes.pbsBashHelper]
		self._makeNote('qsub cmdline: ' + subprocess.list2cmdline(cmdList))
		if not self.dryRun:
			subprocess.check_call(cmdList)

	def _getGridString(self):
		if self.grid is None:
			return 'None'
		else:
			return self.grid.toCompactString()

	def _getConditionsString(self):
		return shared.translators.listOfDictionaries2CompactString(self.experimentalConditions)

	def _waitForCompletion(self):
		if not self.dryRun:
			while subprocess.check_output([pbsEnv.qstat, '-u', pbsEnv.user]) != '':
				sleep(pbsEnv.qstatCheckingPeriod)

	@abstractmethod
	def processResults(self):
		pass

	def executeAtEveryExperimentDir(self, function, cargs, kwargs):
		'''The function must accept a grid point parameter dictionary as its first argument'''
		for gridPoint in self.grid:
			gpDirName = shared.translators.dictionary2FilesystemName(gridPoint)
			try:
				os.chdir(gpDirName)
				args = (gridPoint,) + cargs
				function(*args, **kwargs)
				os.chdir('..')
			except OSError as err:
					print('\033[93mWarning!\033[0m Could not enter directory \033[1m' + err.filename + '\033[0m')

	def executeAtEveryConditionsDir(self, condFunc, condCArgs, condKWArgs):
		'''Function condFunc must accept a grid point parameter dictionary as its first
       argument and a conditions parameter dictionary as its second argument.
		'''
		def executeAtEveryConditionsDir(gridPoint, expObj, function, cargs, kwargs):
			for condPoint in expObj.experimentalConditions:
				condDirName = shared.translators.dictionary2FilesystemName(condPoint)
				try:
					os.chdir(condDirName)
					args = (gridPoint, condPoint) + cargs
					function(*args, **kwargs)
					os.chdir('..')
				except OSError as err:
					print('\033[93mWarning!\033[0m Could not enter directory \033[1m' + err.filename + '\033[0m')
		condArgs = (self, condFunc, condCArgs, condKWArgs)
		self.executeAtEveryExperimentDir(executeAtEveryConditionsDir, condArgs, {})

	def addResultRecord(self, resultsFileName, paramsDict, resultsDict):
		'''Appends a record to a results accumulating file. Can be exeuted from
       any point. File format:
         # paramsKey0 ... paramsKeyN resultsKey0 ... resultsKeyM
         paramsVal0 ... paramsValN resultsVal0 ... resultsValM
       The header comment is only added when the function is called for the
       first time, the result lines are only appended afterwards.
       If the function is called with a different set of parameter/result
       names than the one used in the intial call, ValueError is raised.
       For best results, keep the keys short (under 20 symbols).'''
		numDecimals = 13
		numReprWidth = numDecimals + 7

		def addResultFileHeader(file, params, results):
			file.write('#')
			initialShift = 2
			for paramName in params.keys():
				paramNameStr = paramName.ljust(numReprWidth - initialShift, ' ')
				initialShift = 0
				file.write(' ' + paramNameStr)
			for resultName in results.keys():
				resultNameStr = resultName.ljust(numReprWidth, ' ')
				file.write(' ' + resultNameStr)
			resultsFile.write('\n')
		def addResultLine(file, params, results):
			leadingSpaces = 0
			for paramVal in params.values():
				paramValStr = ( '%.' + str(numDecimals) + 'e' ) % paramVal
				paramValStr = paramValStr.rjust(numReprWidth, ' ')
				file.write(' '*leadingSpaces + paramValStr)
				leadingSpaces = 1
			for resultVal in results.values():
				resultValStr = ( '%.' + str(numDecimals) + 'e' ) % resultVal
				resultValStr = resultValStr.rjust(numReprWidth, ' ')
				file.write(' ' + resultValStr)
			file.write('\n')

		with open(os.path.join(self._resultsDir, resultsFileName), 'a') as resultsFile:
			if self._resultsFiles.has_key(resultsFileName):
				origParamNames, origResultNames = self._resultsFiles[resultsFileName]
				if paramsDict.keys() != origParamNames or resultsDict.keys() != origResultNames:
					print 'Reprs: orig param ' + repr(origParamsDict) + ' new param ' + repr(paramsDict) + ' orig results ' + repr(origResultsDict) + ' new results ' + repr(resultsDict) + '\n'
					raise ValueError('Error: trying to write heterogenous data into ' + resultsFileName)
			else:
				addResultFileHeader(resultsFile, paramsDict, resultsDict)
				self._resultsFiles[resultsFileName] = (paramsDict.keys(), resultsDict.keys())
			addResultLine(resultsFile, paramsDict, resultsDict)

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
			pathVerRecord(verFile, 'evs', routes.evsHome)
			pathVerRecord(verFile, 'client', routes.clientHome)