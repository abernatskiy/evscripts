#!/usr/bin/python2

import staticEvsDynamicCeExperiment as sedce
import shared.grid

e = sedce.staticEvsDynamicCeExperiment('lpecoarse20151015',
			[{'linearDrag':0.0, 'angularDrag':0.0}, {'linearDrag':0.2, 'angularDrag':0.2}],
			grid=shared.grid.LogLinGrid([['sensorGain', 'log', 4.0, 4.0, 1, 1], ['forceGain', 'log', 0.8, 4.0, 2, 2]]),
			pointsPerJob=2
			)

e.run()
