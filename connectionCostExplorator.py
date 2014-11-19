#!/usr/bin/python2

from subprocess import call
from math import pow

# fg 16 sg 4 - classical Braitenberg
# fg 8 sg 2 - nonmodular Braitenberg, with classical one performing suboptimally

forceGain = 8.0
sensorGain = 2.0
randomSeedsFile = 'randints1416376705.dat'

connectionCost = 0.0
print('Investigating the case of forceGain ' + str(forceGain) + ', sensorGain ' + str(sensorGain) + ', connection cost ' + str(connectionCost))
call(['./getFitnessTimeSeriesForParams.sh', str(forceGain), str(sensorGain), str(connectionCost), randomSeedsFile])

for connectionCost in [pow(2.0, x) for x in range(4, 16)]:
	print('Investigating the case of forceGain ' + str(forceGain) + ', sensorGain ' + str(sensorGain) + ', connection cost ' + str(connectionCost))
	call(['./getFitnessTimeSeriesForParams.sh', str(forceGain), str(sensorGain), str(connectionCost), randomSeedsFile])
