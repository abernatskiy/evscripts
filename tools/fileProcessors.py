import subprocess
import sys
sys.path.append('..')
import routes
import imp
sysEnv = imp.load_source('sysEnv', routes.sysEnv)

def extractColumn(path, field, offset=0, dtype=float):
	cutOut = subprocess.check_output([sysEnv.cut, '-d', ' ', '-f', str(field), path])
	valStrs = [ s for s in cutOut.split('\n')[offset:] if s != '' ]
	return map(dtype, valStrs)

def extractColumnFromEVSLogs(path, field, dtype=float):
	return extractColumn(path, field, offset=3, dtype=dtype)

def randSeedList(randSeedPath, size=None):
	with open(randSeedPath, 'r') as randSeedFile:
		randSeedStr = randSeedFile.read()
	if size:
		if len(randSeedStr) < size:
			raise ValueError('Random seed library is too small to perform the experiment: ' +
												str(size) + 'values requested, ' +
												str(len(randSeedStr)) + ' available at ' + randSeedPath)
		randSeedStr = randSeedStr[:size]
	return map(int, randSeedStr.split())
