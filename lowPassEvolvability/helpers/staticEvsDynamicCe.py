#!/usr/bin/python2

import subprocess
import imp
import os
import sys

from helper import Helper
from helper import dict2DirName

class SEDCHelper(Helper):
	def __init__(self, argv):
		super(Helper, self).__init__(argv)
		self.sysEnv = imp.load_source('sysEnv', self.routes.sysEnv)

	def _runGroup(self, fcond):
		super(Helper, self)._runGroup(fcond)
		self._makeFIFOs()
		self._spawnClient(fcond)
		self._runServer()
		self._killClient()
		self._removeFIFOs()
		self._preprocessResults()

	def _makeFIFOs(self):
		subprocess.call([self.sysEnv.mkfifo, 'genes'])
		subprocess.call([self.sysEnv.mkfifo, 'evals'])
		curDir = os.getcwd()
		self.genesPipe = os.path.join(curDir, 'genes')
		self.evalsPipe = os.path.join(curDir, 'evals')

	def _spawnClient(self, fcond):
		clientBinary = os.path.join(self.rootDir, 'bin', 'cylindersEvasion_' + dict2DirName(fcond))
		self.clientProc = subprocess.Popen([clientBinary, self.genesPipe, self.evalsPipe])

	def _runServer(self):
		configPath = os.path.join(self.rootDir, 'config.ini')
		subprocess.check_call([sys.executable, self.routes.evsExecutable, self.evalsPipe, self.genesPipe, 9001, configPath])

	def _killClient(self):
		self.clientProc.send_signal(subprocess.signal.SIGTERM)

	def _removeFIFOs(self):
		subprocess.call([self.sysEnv.rm, self.genesPipe])
		subprocess.call([self.sysEnv.rm, self.evalsPipe])

	def _preprocessResults(self):
		pass

if __name__ == '__main__':
	f = open('helpernotes.txt', 'w')
	f.write('Arguments: ' + str(sys.argv) + '\n')
	f.write('Attempting to create Helper...\n')
	f.flush()
	h = Helper(sys.argv)
	f.write(str(h))
	f.close()
	h.runExperiments()
	print('DONE')
