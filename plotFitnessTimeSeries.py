#!/usr/bin/python2

import numpy as np
import matplotlib.pyplot as plt

def plotFitnessTS(filename, plotColor):
	fitnessTS = np.loadtxt(filename)
	fitnessMeanTS = np.mean(fitnessTS, axis=0)
	fitnessStdTS = np.std(fitnessTS, axis=0)

	fitnessLower = fitnessMeanTS - fitnessStdTS
	fitnessUpper = fitnessMeanTS + fitnessStdTS

	gens = np.arange(0,len(fitnessMeanTS))

	plt.xlabel('Generations')
	plt.ylabel('Fitness')

	plt.plot(gens, fitnessLower, gens, fitnessUpper, color=plotColor, alpha=0.5)
	plt.fill_between(gens, fitnessLower, fitnessUpper, where=fitnessUpper>=fitnessLower, facecolor=plotColor, alpha=0.3, interpolate=True)
	plt.plot(gens, fitnessMeanTS, color=plotColor)

#plotFitnessTS('fg16.0sg4.0cc0.0_fitnessTimeSeries.dat', 'red')

files1k = [ 'fg8.0sg2.0cc32768.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc16384.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc8192.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc4096.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc2048.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc1024.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc512.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc256.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc128.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc64.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc32.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc16.0_fitnessTimeSeries.dat', \
          'fg8.0sg2.0cc0.0_fitnessTimeSeries.dat' ]
