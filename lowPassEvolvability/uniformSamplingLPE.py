#!/usr/bin/python2

import os
import numpy as np
import subprocess

import staticEvsDynamicCeExperiment as sedce
import shared.grid

def _extractFitness(filename):
	strFitnessVals = subprocess.check_output(['/usr/bin/cut', '-d', ' ', '-f', '1', filename])
	return np.fromstring(strFitnessVals[6:], sep='\n')

def _readFitnessIncrements(files):
	fitness = [ _extractFitness(file) for file in files ]
	return (fitness[1] - fitness[0])/fitness[0]

def _readFitnessDifferences(files):
	fitness = [ _extractFitness(file) for file in files ]
	return np.abs(fitness[1] - fitness[0])/fitness[0]

class uniformSamplingLPEExperiment(sedce.staticEvsDynamicCeExperiment):
	def processResults(self):
		def processDir(gridPoint, condPoint, self):
			fileNameBase = 'population' + str(int(gridPoint['randomSeed'])) + '_gen'
			files = [ fileNameBase + '0.log', fileNameBase + '1.log' ]
			inc = _readFitnessIncrements(files)
			diff = _readFitnessDifferences(files)
			def stderr(samples):
				return np.std(samples)/np.sqrt(float(len(samples)))
			print repr((np.mean(inc), stderr(inc), np.mean(diff), stderr(inc)))
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
						'populationSize = 10\n'
						'logPopulation = yes\n')

if __name__ == '__main__':
	e = uniformSamplingLPEExperiment('uniformSamplingLPE20151027',
				[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
				grid=shared.grid.LogLinGrid([['sensorGain', 'log', 4.0, 4.0, 1, 1], ['forceGain', 'log', 0.8, 4.0, 1, 1]]),
				pointsPerJob=4,
				expectedWallClockTime='00:10:00')
#	e.run()
	e.enterWorkDir()
	e.processResults()
	e.exitWorkDir()
