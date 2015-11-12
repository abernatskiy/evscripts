#!/usr/bin/python2

import os
import numpy as np
import subprocess

import staticEvsDynamicCeExperiment as sedce
import shared.grid
from copy import copy

def extractFitness(filename):
	strFitnessVals = subprocess.check_output(['/usr/bin/cut', '-d', ' ', '-f', '1', filename])
	return np.fromstring(strFitnessVals[6:], sep='\n')

def stderr(samples):
	return np.std(samples)/np.sqrt(float(len(samples)))

def recordEvolvabilityStats(fullCond, fitness, experiment):
	inc = (fitness[1] - fitness[0])/fitness[0]
	diff = np.abs(fitness[1] - fitness[0])/fitness[0]

	results = {}
	results['incMean'] = np.mean(inc)
	results['incStdErr'] = stderr(inc)
	experiment.addResultRecord('increments.dat', fullCond, results)

	results = {}
	results['diffMean'] = np.mean(diff)
	results['diffStdErr'] = stderr(diff)
	experiment.addResultRecord('differences.dat', fullCond, results)

def chunks(l, n):
	'''Yield successive n-sized chunks from l.'''
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def chunkedMaxStats(fitness, numChunks):
	if len(fitness[0]) % numChunks != 0:
		raise ValueError('Number of fitness records (' + str(len(fitness)) + ')  must be divisible by the number of chunks (' + str(numChunks) + ')')
	lenChunk = len(fitness[0])/numChunks
	fitChunks = chunks(fitness[0], lenChunk)
	fitMax = map(np.max, fitChunks)
	return (np.mean(fitMax), np.std(fitMax))

def recordRandomSearchStats(fullCond, fitness, experiment):
	results = {}
	for nc in [1, 10, 100, 1000]:
		mean, std = chunkedMaxStats(fitness, nc)
		results['mean' + str(nc)] = mean
		results['std' + str(nc)] = std
	experiment.addResultRecord('randomSearchStats.dat', fullCond, results)

class uniformSamplingLPEExperiment(sedce.staticEvsDynamicCeExperiment):
	def processResults(self):
		def processDir(gridPoint, condPoint, self):
			fileNameBase = 'population' + str(int(gridPoint['randomSeed'])) + '_gen'
			files = [ fileNameBase + '0.log', fileNameBase + '1.log' ]
			fitness = [ extractFitness(file) for file in files ]

			fullCond = copy(gridPoint)
			fullCond.update(condPoint)

			recordEvolvabilityStats(fullCond, fitness, self)
			recordRandomSearchStats(fullCond, fitness, self)
		self.executeAtEveryConditionsDir(processDir, (self,), {})

	def evsConfig(self):
		return ('[classes]\n'
						'individual = trinaryVectorSureMutation\n'
						'communicator = chunkedUnixPipe\n'
						'evolver = evolvabilityMeasurerUniformSampling\n'
						'\n'
						'[indivParams]\n'
						'length = 60\n'
						'\n'
						'[evolParams]\n'
						'populationSize = 100000\n'
						'logPopulation = yes\n')

def initializeExperiment():
	return uniformSamplingLPEExperiment('uniformSamplingLPE201511103',
				[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
				grid=shared.grid.LogLinGrid([['sensorGain', 'log', 16.0, 4.0, 1, 1], ['forceGain', 'log', 0.8, 4.0, 2, 2]]),
				pointsPerJob=1,
				expectedWallClockTime='03:00:00')

if __name__ == '__main__':
	e = initializeExperiment()
	e.run()
