#!/usr/bin/python2

import staticEvsDynamicCeExperiment as sedce
import shared.grid

e = sedce.staticEvsDynamicCeExperiment('testExperiment',
			[{'forceGain':0.0}, {'forceGain':100.0}],
			grid=shared.grid.Grid(['sensorGain', 'firstOrderDynamics'], [[0,1], [0,1]]),
			pointsPerJob=2
	)

e.run()
