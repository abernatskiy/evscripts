#PBS -l nodes=1:ppn=1
#PBS -N experimentJob
#PBS -j n
#PBS -m a

cd $PBS_O_WORKDIR
echo "This is experimentJob running on " `hostname`
$PYTHON $PYTHON_HELPER $PBS_ARRAYID $GRID
