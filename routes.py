from os.path import expanduser, join

home = expanduser('~')
evscriptsHome = join(home, 'evscripts')

sysEnv = join(evscriptsHome, 'environment/os', 'gentoo.py')
pbsEnv = join(evscriptsHome, 'environment/host', 'vacc.py')
