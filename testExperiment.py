#!/usr/bin/python2

import grid
import experiment

class CertainExperiment(experiment.Experiment):
	def prepareEnv(self):
		super(CertainExperiment, self).prepareEnv()
	def processResults(self):
		pass

if __name__ == '__main__':
	g = grid.Grid1d('paramName', [1,2,3])
	print 'Grid: ' + str(g)
	print 'Attempting to make an Experiment...'
	e = CertainExperiment('certainExperiment0', g, dryRun=True)
	e.run()
