from os.path import expanduser, join

home = expanduser('~')
evscriptsHome = join(home, 'evscripts')

envHome = join(evscriptsHome, 'env')
sysEnv = join(envHome, 'sysGentoo.py')
pbsEnv = join(envHome, 'pbsVacc.py')

helpersHome = join(evscriptsHome, 'helpers')
pbsBashHelper = join(helpersHome, 'pbsVaccSubmittable.sh')
pbsPythonHelper = join(helpersHome, 'staticEvsDynamicCeHelper.py')

clientHome = join(home, 'cylindersEvasion')
evsHome = join(home, 'evs')
evsExecutable = join(evsHome, 'mainConfig.py')

sedcSettings = join(evscriptsHome, 'shared', 'staticEvsDynamicCeForLowPassEvolvability.py')
