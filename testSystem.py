#!/usr/bin/python2

'''Small modification of uniformSampligLPE.py intended for debugging the system'''

import os
import numpy as np
import subprocess

import staticEvsDynamicCeExperiment as sedce
from shared.grid import LogGrid,Grid1d

import tools.fileProcessors as tfp
import tools.stats as ts
import tools.algorithms as ta

def extractFitness(filename):
	return np.array(tfp.extractColumnFromEVSLogs(filename, 1))

class testExperiment(sedce.staticEvsDynamicCeExperiment):
	def processResults(self):
		def processDir(gridPoint, condPoint, self):
			fileNameBase = 'population' + str(int(gridPoint['randomSeeds'])) + '_gen'
			files = [ fileNameBase + '0.log', fileNameBase + '1.log' ]
			fitness = [ extractFitness(file) for file in files ]
			fullCond = ta.sumOfDicts(gridPoint, condPoint)

			self._recordEvolvabilityStats(fullCond, fitness)
			self._recordRandomSearchStats(fullCond, fitness)

#		self.executeAtEveryConditionsDir(processDir, (self,), {})
		pass

	def _recordRandomSearchStats(self, fullCond, fitness):
		results = {}
		for nc in [1, 10, 100, 1000]:
			mean, std = ts.chunkedMaxStats(fitness, nc)
			results['mean' + str(nc)] = mean
			results['std' + str(nc)] = std
		self.addResultRecord('randomSearchStats.dat', fullCond, results)

	def _recordEvolvabilityStats(self, fullCond, fitness):
		inc = (fitness[1] - fitness[0])/fitness[0]
		diff = np.abs(fitness[1] - fitness[0])/fitness[0]

		results = {}
		results['incMean'] = np.mean(inc)
		results['incStdErr'] = ts.stderr(inc)
		self.addResultRecord('increments.dat', fullCond, results)

		results = {}
		results['diffMean'] = np.mean(diff)
		results['diffStdErr'] = ts.stderr(diff)
		self.addResultRecord('differences.dat', fullCond, results)

	def evsConfig(self):
		return ('[classes]\n'
						'individual = trinaryVectorSureMutation\n'
						'communicator = chunkedUnixPipe\n'
						'evolver = proportionalEvolver\n'
						'\n'
						'[indivParams]\n'
						'length = 60\n'
						'\n'
						'[evolParams]\n'
						'populationSize = 200\n'
						'logPopulation = yes\n'
						'backup = yes\n'
						'backupPeriod = 100\n'
						'genStopAfter = 10000\n')

def baseGrid():
	sgGrid = LogGrid('sensorGain', 16, 4, 0, 0)
	fgGrid = LogGrid('forceGain', 0.8, 4, 1, 1)
	return sgGrid*fgGrid

def initializeExperiment():
	grid = baseGrid()
	grid += Grid1d('randomSeeds', [9001]*len(grid))
	return testExperiment('testExperiment20151202',
				[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
				grid=grid,
				pointsPerJob=1,
				queue='shortq',
				expectedWallClockTime='00:10:00',
				repeats=2)

if __name__ == '__main__':
	e = initializeExperiment()
	e.run()
