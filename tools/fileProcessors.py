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
