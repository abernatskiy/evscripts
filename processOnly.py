#!/usr/bin/python2

import argparse
cliParser = argparse.ArgumentParser(description='Run only the data processing part of any experiment. The experiment-defining file must define initializeExperiment() function.')
cliParser.add_argument('experimentScript', metavar='experimentScript', type=str, help='executable file of the experiment of interest')
cliArgs = cliParser.parse_args()

import imp
experimentDesc = imp.load_source('nothing', cliArgs.experimentScript)

e = experimentDesc.initializeExperiment()
e.enterWorkDir()
import os
print os.getcwd()
e.processResults()
e.exitWorkDir()
