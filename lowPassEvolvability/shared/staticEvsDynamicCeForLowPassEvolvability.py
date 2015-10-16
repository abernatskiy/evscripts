import subprocess
import numpy as np

def _extractFitness(filename):
	strFitnessVals = subprocess.check_output(['/usr/bin/cut', '-d', ' ', '-f', '1', filename])
	return np.fromstring(strFitnessVals[6:], sep='\n')

def _fitnessIncrements(files):
	fitness = [ _extractFitness(file) for file in files ]
	relDiff = np.vectorize(lambda x,y: 0 if x==y and y==0 else (y-x)/x)
	return relDiff(fitness[0], fitness[1])

def preprocessData(dict):
	def fileName(num):
		return 'population' + str(int(dict['randomSeed'])) + '_gen' + str(num) + '.log'
	files = [ fileName(i) for i in [0,1] ]
	fitnessIncrements = _fitnessIncrements(files)
	np.savetxt('fitnessIncrements.dat', fitnessIncrements)

def createEvsConfig():
	f = open('config.ini', 'w')
	f.write('[classes]\n'
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
	f.close()
