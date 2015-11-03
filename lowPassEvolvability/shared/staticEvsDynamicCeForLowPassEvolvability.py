import numpy as np

def preprocessData(dict):
	def fileName(num):
		return 'population' + str(int(dict['randomSeed'])) + '_gen' + str(num) + '.log'
	files = [ fileName(i) for i in [0,1] ]
	fitnessIncrements = _fitnessIncrements(files)
	np.savetxt('fitnessIncrements.dat', fitnessIncrements)
