from os.path import expanduser, join

home = expanduser('~')
evscriptsHome = join(home, 'evscripts/lowPassEvolvability')
envHome = join(evscriptsHome, 'env')

sysEnv = join(envHome, 'sysGentoo.py')
pbsEnv = join(envHome, 'pbsVacc.py')
