#!/usr/bin/python2

# A script which takes rawData.ssv and spits out files with fields of values
# Values I need:
# mean fitness
# relative error (stddev/mean fitness)
# symmetricity
# no of connections

import numpy as np

class Network(object):
	def __init__(self, arr):
		self.weights = map(int, arr)
	def __eq__(self, other):
		return self.weights == other.weights
	def isSymmetrical(self):
		'Checks if vector of weights is invariant under reversal'
		return self.weights == self.weights[::-1]
	def nonZeroWeights(self):
		return len(self.weights) - self.weights.count(0)

class Run(object):
	def __init__(self, arr):
		self.seed = int(arr[0].rstrip(':').lstrip('seed'))
		self.bestFitness = float(arr[1])
		self.id = int(arr[2])
		self.network = Network(arr[3:7])

class Record(object):
	def __init__(self, strings):
		strings = line.split()
		self.forceGain = float(strings[1])
		self.sensorGain = float(strings[3])
		noOfRuns = (len(strings)-4)/7 # four fields for params data, seven fields per run
		self.runs = []
		for runNo in xrange(0, noOfRuns): 
			self.runs.append(Run(strings[4+7*runNo:11+7*runNo]))
	def __repr__(self):
		return str(self)
	def __str__(self):
		return 'forceGain: ' + str(self.forceGain) + ' sensorGain: ' + str(self.sensorGain) + ' noOfRuns: ' + str(len(self.runs)) 

records = []

file = open('rawResults.ssv', 'r')
for line in file:
	records.append(Record(line.split(' ')))
file.close()
