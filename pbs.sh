#PBS -l nodes=1:ppn=1
#PBS -N experimentJob
#PBS -j n
#PBS -m a

cd $PBS_O_WORKDIR
echo "This is pbs.sh running on `hostname`"
echo "Starting a worker with command line $PYTHON ${EVSCRIPTS_HOME}/helper.py $PARENT_SCRIPT $POINT_PER_JOB"
$PYTHON ${EVSCRIPTS_HOME}/worker.py $PARENT_SCRIPT $POINT_PER_JOB
