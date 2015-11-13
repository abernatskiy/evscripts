#!/usr/bin/python2

import os
import numpy as np
import subprocess

import staticEvsDynamicCeExperiment as sedce
import shared.grid
from copy import copy

#def _extractFitness(filename):
#	strFitnessVals = subprocess.check_output(['/usr/bin/cut', '-d', ' ', '-f', '1', filename])
#	return np.fromstring(strFitnessVals[6:], sep='\n')
#
#def _readFitnessIncrements(files):
#	fitness = [ _extractFitness(file) for file in files ]
#	return (fitness[1] - fitness[0])/fitness[0]
#
#def _readFitnessDifferences(files):
#	fitness = [ _extractFitness(file) for file in files ]
#	return np.abs(fitness[1] - fitness[0])/fitness[0]

class runLPEExperiment(sedce.staticEvsDynamicCeExperiment):
	def processResults(self):
#		def processDir(gridPoint, condPoint, self):
#			fileNameBase = 'population' + str(int(gridPoint['randomSeed'])) + '_gen'
#			files = [ fileNameBase + '0.log', fileNameBase + '1.log' ]
#
#			inc = _readFitnessIncrements(files)
#			diff = _readFitnessDifferences(files)
#
#			fullCond = copy(gridPoint)
#			fullCond.update(condPoint)
#			def stderr(samples):
#				return np.std(samples)/np.sqrt(float(len(samples)))
#
#			results = {}
#			results['incMean'] = np.mean(inc)
#			results['incStdErr'] = stderr(inc)
#			self.addResultRecord('increments.dat', fullCond, results)
#
#			results = {}
#			results['diffMean'] = np.mean(diff)
#			results['diffStdErr'] = stderr(diff)
#			self.addResultRecord('differences.dat', fullCond, results)
#		self.executeAtEveryConditionsDir(processDir, (self,), {})
		pass

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
						'populationSize = 10\n'
						'eliteSize = 1\n'
						'logBestIndividual = yes\n'
						'genStopAfter = 10\n')

def initializeExperiment():
	exp = runLPEExperiment('runLPE201511106',
				[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
#				grid=shared.grid.LogLinGrid([['sensorGain', 'log', 16.0, 4.0, 1, 1], ['forceGain', 'log', 0.8, 4.0, 2, 2]]),
				grid=shared.grid.LogLinGrid([['sensorGain', 'log', 16.0, 4.0, 1, 1], ['forceGain', 'log', 0.8, 4.0, 0, 0]]),
				pointsPerJob=2,
#				dryRun=True,
				expectedWallClockTime='00:30:00')
	return exp

if __name__ == '__main__':
	e = initializeExperiment()
	e.run()
