#!/usr/bin/python2

import numpy as np
import subprocess

def _extractFitness(filename):
	strFitnessVals = subprocess.check_output(['/usr/bin/cut', '-d', ' ', '-f', '1', filename])
	return np.fromstring(strFitnessVals[6:], sep='\n')

def readFitnessIncrements(files):
	fitness = [ _extractFitness(file) for file in files ]
	return (fitness[1] - fitness[0])/fitness[0]

#files = ['population236_gen0.log', 'population236_gen1.log']
#fitInc = readFitnessIncrements(files)
