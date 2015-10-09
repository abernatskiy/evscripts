#!/usr/bin/python2

import experiment
import grid
e = experiment.Experiment('testExperiment',
			[{'brightness':0, 'contrast':0}, {'brightness':100, 'contrast':100}],
			expectedWallClockTime='00:01:00',
			grid=grid.Grid(['a', 'b'], [[0.1, 1], [2, 3]]),
			pointsPerJob=2)
e.run()

