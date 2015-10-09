#!/usr/bin/python2

import experiment
e = experiment.Experiment('testExperiment', [{'brightness':0, 'contrast':0}, {'brightness':100, 'contrast':100}], expectedWallClockTime='00:01:00')
e.run()

