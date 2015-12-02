# pbsEnv environmental file
# Information on VACC queues and binaries

user = 'abernats'
qsub = '/opt/pbs/bin/qsub'
qstat = '/opt/pbs/bin/qstat'
qstatCheckingPeriod = 120
defaultQueue = 'shortq'
queueLims = {'shortq': '03:00:00', 'workq': '30:00:00', 'ibq': '30:00:00'}
maxRootNodeThreads = 6 # now many root node CPUs we're allowed to to prepare runtime environment/process results
                       # VACC rootnode has 12 CPUs, I'll take a half
