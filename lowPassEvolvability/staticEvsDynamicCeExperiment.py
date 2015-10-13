import os
import subprocess
import imp
from copy import copy

import routes
import shared.grid
import shared.translators
from experiment import Experiment

sysEnv = imp.load_source('sysEnv', routes.sysEnv)

numProcsForMake = 6 # VACC rootnode has 12 CPUs, I'll take a half

def _dictionary2CeGccOptions(dict):
	numericalParams = {	'angularGain': 'ANGULAR_GAIN',
											'forceGain': 'FORCE_GAIN',
											'sensorGain': 'SENSOR_GAIN',
											'robotRadius': 'ROBOT_RADIUS',
											'robotHeight': 'RHEIGHT',
											'linearDrag': 'LINEAR_DRAG_COEFFICIENT',
											'angularDrag': 'ANGULAR_DRAG_COEFFICIENT',
											'tailScale': 'TAIL_SCALE' }
	booleanParams = {	'firstOrderDynamics': 'FIRST_ORDER_DYNAMICS',
										'withOcclusion': 'WITH_OCCLUSION',
										'withGraphics': 'WITH_GRAPHICS',
										'withScreenshots': 'WITH_SCREENSHOTS' }
	ignoreParams = ['randomSeed'] # FIXME
	def paramString(paramName, dict):
		if paramName in numericalParams:
			return '-D' + numericalParams[paramName] + '=' + str(dict[paramName])
		elif paramName in booleanParams:
			return '-D' + booleanParams[paramName] if dict[paramName] != 0.0 else ''
		elif paramName in ignoreParams:
			return ''
		else:
			raise ValueError('Unrecognized parameter ' + paramName)
	return ' '.join([ paramString(paramName, dict) for paramName in dict.keys() ])

class staticEvsDynamicCeExperiment(Experiment):
	def _prepareEnv(self):
		super(staticEvsDynamicCeExperiment, self)._prepareEnv()
		self._createEvsConfig()
		self._prepareClientBinaries()

	def _createEvsConfig(self):
		f = open('config.ini', 'w')
		f.write('[classes]\n'
						'individual = trinaryVectorSureMutation\n'
						'communicator = chunkedUnixPipe\n'
						'evolver = evolvabilityMeasurerUniformSampling\n'
						'\n'
						'[indivParams]\n'
						'length = 60\n'
						'\n'
						'[evolParams]\n'
						'populationSize = 10\n'
						'logPopulation = yes\n')
		f.close()

	def _prepareClientBinaries(self):
		mainExpDir = os.getcwd()
		os.makedirs('bin')
		os.chdir(routes.clientHome)
		for gridParams in self.grid:
			for experimentalParams in self.experimentalConditions:
				fullParams = copy(gridParams)
				fullParams.update(experimentalParams)
				clientBinaryPath = os.path.join(mainExpDir, 'bin', 'cylindersEvasion_' + shared.translators.dictionary2FilesystemName(fullParams))
				self._compileClient(fullParams, clientBinaryPath)
		os.chdir(mainExpDir)

	def _compileClient(self, params, outPath):
		'''Must operate at routes.clientHome directory'''
		optionsStr = _dictionary2CeGccOptions(params)

		FNULL = open(os.devnull, 'w')
		logFile = open(outPath + '.makestderr', 'w')

		subprocess.check_call([sysEnv.make, 'clean'], stdout=FNULL)
		subprocess.check_call(sysEnv.make + ' -j' + str(numProcsForMake) + ' MORECFLAGS="' + optionsStr + '"' , shell=True, stdout=FNULL, stderr=logFile)

		logFile.close()
		FNULL.close()

		os.rename('cylindersEvasion', outPath)
