#!/usr/bin/python2

import numpy as np
import matplotlib.pyplot as plt
import os
import fnmatch

def plotFitnessTS(filename, plotColor, plotStd=True):
	fitnessTS = np.loadtxt(filename)
	fitnessMeanTS = np.mean(fitnessTS, axis=1)
	fitnessStdTS = np.std(fitnessTS, axis=1)*1.96/np.sqrt(float(fitnessTS.shape[1]))

	fitnessLower = fitnessMeanTS - fitnessStdTS
	fitnessUpper = fitnessMeanTS + fitnessStdTS

	gens = np.arange(0,len(fitnessMeanTS))

	plt.xlabel('Generations')
	plt.ylabel('Fitness')

	if plotStd:
		plt.plot(gens, fitnessLower, gens, fitnessUpper, color=plotColor, alpha=0.5)
		plt.fill_between(gens, fitnessLower, fitnessUpper, where=fitnessUpper>=fitnessLower, facecolor=plotColor, alpha=0.3, interpolate=True)
	plt.plot(gens, fitnessMeanTS, color=plotColor, label=filename)

#plotFitnessTS('fg16.0sg4.0cc0.0_fitnessTimeSeries.dat', 'red')

colors = ['black', 'red', 'yellow', 'green', 'cyan', 'blue', 'violet']
#colors = ['red', 'green', 'cyan', 'blue', 'violet']
colorIdx = 0

files = ['espinosa-soto', 'random_expl0.5_insdel0.5', 'random_expl0.5_insdel1.0', 'random_expl0.5_insdel2.0', 'sparse_expl0.5_insdel0.5', 'sparse_expl0.5_insdel1.0', 'sparse_expl0.5_insdel2.0']
#files = ['random_expl0.5_insdel0.5', 'random_expl0.5_insdel1.0', 'random_expl0.5_insdel2.0']
#files = ['sparse_expl0.5_insdel0.5', 'sparse_expl0.5_insdel1.0', 'sparse_expl0.5_insdel2.0']
#files = ['random_expl0.5_insdel1.0', 'sparse_expl0.5_insdel1.0', 'espinosa-soto']
for file in files:
	plotFitnessTS(file + '.qvalue', colors[colorIdx], plotStd=True)
#	plotFitnessTS(file, colors[colorIdx])
	colorIdx = (colorIdx + 1) % 7

#plt.legend(loc=4) # for fitness
plt.legend(loc=1) # for Q
plt.title('Q vs time')
plt.xlim(0,2000)
#plt.show()
