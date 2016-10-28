from os.path import expanduser, join

home = expanduser('~')
evscriptsHome = join(home, 'evscripts')

envHome = join(evscriptsHome, 'env')
sysEnv = join(envHome, 'sysGentoo.py')
pbsEnv = join(envHome, 'pbsVacc.py')

workersHome = evscriptsHome
pbsBashWorker = join(helpersHome, 'pbs.sh')

clientHome = join(home, 'cylindersEvasion')
evsHome = join(home, 'evs')
evsExecutable = join(evsHome, 'evsServer.py')
evsResume = join(evsHome, 'evsContinue.py')
