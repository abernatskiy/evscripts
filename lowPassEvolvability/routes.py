from os.path import expanduser, join

home = expanduser('~')
evscriptsHome = join(home, 'evscripts', 'lowPassEvolvability')

envHome = join(evscriptsHome, 'env')
sysEnv = join(envHome, 'sysGentoo.py')
pbsEnv = join(envHome, 'pbsVacc.py')

helpersHome = join(evscriptsHome, 'helpers')
pbsBashHelper = join(helpersHome, 'pbsVaccSubmittable.sh')
pbsPythonHelper = join(helpersHome, 'staticEvsDynamicCeHelper.py')

evsExecutable = join(home, 'evs', 'mainConfig.py')
clientHome = join(home, 'cylindersEvasion')
