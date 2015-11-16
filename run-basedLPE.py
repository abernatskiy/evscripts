#!/usr/bin/python2

import os
import numpy as np
import subprocess

import staticEvsDynamicCeExperiment as sedce
from shared.grid import LogGrid,Grid1d
from copy import copy

class runLPEExperiment(sedce.staticEvsDynamicCeExperiment):
	def processResults(self):
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
	sgGrid = LogGrid('sensorGain', 16, 4, 1, 1)
	fgGrid = LogGrid('forceGain', 0.8, 4, 2, 2)
	paramGrid = sgGrid*fgGrid

	rsGrid = Grid1d('randomSeeds', [[9001, 9002, 9003]]*len(paramGrid))
	paramGrid += rsGrid

	exp = runLPEExperiment('runLPE20151115',
				[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
				grid=paramGrid,
				pointsPerJob=2,
#				dryRun=True,
				expectedWallClockTime='00:30:00')
	return exp

if __name__ == '__main__':
	e = initializeExperiment()
	e.run()
