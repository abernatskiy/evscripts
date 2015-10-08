#PBS -l nodes=1:ppn=1
#PBS -N experimentJob
#PBS -j n
#PBS -m a

cd $PBS_O_WORKDIR
echo "This is experimentJob running on " `hostname`
$PYTHON $PYTHON_HELPER $EVSCRIPTS_HOME $PBS_ARRAYID $CONDITIONS $GRID $POINTS_PER_JOB
