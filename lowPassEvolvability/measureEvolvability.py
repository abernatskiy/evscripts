#!/usr/bin/python2

import numpy as np
import subprocess

def _extractFitness(filename):
	strFitnessVals = subprocess.check_output(['/usr/bin/cut', '-d', ' ', '-f', '1', filename])
	return np.fromstring(strFitnessVals[6:], sep='\n')

def readFitnessIncrements(files):
	fitness = [ _extractFitness(file) for file in files ]
	return (fitness[1] - fitness[0])/fitness[0]

if __name__ == '__main__':
	import sys
	files = [sys.argv[1], sys.argv[2]]
	fitInc = readFitnessIncrements(files)
	evSamp = len(fitInc)
	evMean = np.mean(fitInc)
	evStdE = np.std(fitInc)/np.sqrt(evSamp)
	print('Evolvability: mean ' + str(evMean) + ', standard error ' + str(evStdE) + ', as measured using ' + str(evSamp) + ' samples')
