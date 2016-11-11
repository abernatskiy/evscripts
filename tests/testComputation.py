from os.path import join

import grid
import routes

# required definitions
computationName = 'testComputation'
parametricGrid = grid.Grid1d('someTruth', [0, 1])
def prepareEnvironment(experiment):
	with open('preparations.txt', 'w') as f:
		f.write('Preparations done!\n')
def processResults(experiment):
	with open('results.txt', 'w') as f:
		f.write('Results processed!\n')
def runComputationAtPoint(worker, params):
	with open('logs.txt', 'w') as f:
		f.write('Computation with params ' + str(params) + ' completed successfully!\n')

# auxiliary definitions
#pointsPerJob = 1
#passes = 1
#queue = 'shortq'
#maxJobs = 1
#expectedWallClockTime = '00:05:00'
#involvedGitRepositories = {'evs': join(routes.home, 'evs')}
#dryRun = True

