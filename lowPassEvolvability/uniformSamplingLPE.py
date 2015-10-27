#!/usr/bin/python2

import staticEvsDynamicCeExperiment as sedce
import shared.grid

class uniformSamplingLPEExperiment(sedce.staticEvsDynamicCeExperiment):
	def processResults(self):
		print 'I got executed!'

	def evsConfig(self):
		return  '[classes]\n'
						'individual = trinaryVectorSureMutation\n'
						'communicator = chunkedUnixPipe\n'
						'evolver = evolvabilityMeasurerUniformSampling\n'
						'\n'
						'[indivParams]\n'
						'length = 60\n'
						'\n'
						'[evolParams]\n'
						'populationSize = 10\n'
						'logPopulation = yes\n'

if __name__ == '__main__':
	e = uniformSamplingLPEExperiment('uniformSamplingLPE20151027',
				[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
				grid=shared.grid.LogLinGrid([['sensorGain', 'log', 4.0, 4.0, 1, 1], ['forceGain', 'log', 0.8, 4.0, 1, 1]]),
				pointsPerJob=4)
	e.run()
