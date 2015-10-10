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
		self._runServer(fcond)
		self._killClient()
		self._ensureProcessesEnd()
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
		cmdList = [clientBinary, self.genesPipe, self.evalsPipe]
		self._makeGroupNote('Starting the client: ' + subprocess.list2cmdline(cmdList) + ' (at ' + os.getcwd() + ')')
#		self.clientProc = subprocess.Popen(cmdList)

	def _runServer(self, fcond):
		configPath = self._getEvsConfig(fcond)
		cmdList = [sys.executable, self.routes.evsExecutable, self.evalsPipe, self.genesPipe, fcond['randomSeed'], configPath]
		self._makeGroupNote('Executing the server: ' + subprocess.list2cmdline(cmdList) + ' (at ' + os.getcwd() + ')')
#		subprocess.check_call(cmdList)

	def _getEvsConfig(self, fcond):
		return os.path.join(self.rootDir, 'config.ini')

	def _killClient(self):
		self._makeGroupNote('Killing the client...')
#		self.clientProc.send_signal(subprocess.signal.SIGTERM)
		pass

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
	h = SEDCHelper(sys.argv)
	f.write(str(h))
	f.close()
	h.runExperiments()
	print('DONE')
