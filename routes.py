from os.path import expanduser, join

home = expanduser('~')
evscriptsHome = join(home, 'evscripts')

envHome = join(evscriptsHome, 'environment')
sysEnv = join(envHome, 'os', 'gentoo.py')
pbsEnv = join(envHome, 'host', 'vacc.py')

pbsBashWorker = join(evscriptsHome, 'pbs.sh')

clientHome = join(home, 'cylindersEvasion')
evsHome = join(home, 'evs')
evsExecutable = join(evsHome, 'evsServer.py')
evsResume = join(evsHome, 'evsContinue.py')
