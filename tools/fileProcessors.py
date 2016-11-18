import subprocess
import sys
sys.path.append('..')
import routes
import imp
sysEnv = imp.load_source('sysEnv', routes.sysEnv)

def extractColumn(path, field, offset=0, dtype=float):
	'''Reads a column (field) from a file (path), ignores some lines (offset), then converts every line of the column into dtype and returns results as a list'''
	cutOut = subprocess.check_output([sysEnv.cut, '-d', ' ', '-f', str(field), path])
	valStrs = [ s for s in cutOut.split('\n')[offset:] if s != '' ]
	return map(dtype, valStrs)
