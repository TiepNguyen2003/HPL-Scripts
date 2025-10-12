#!/bin/bash
#SBATCH --nodes=1    # request nodes
#SBATCH --partition test      # this job will be submitted to short queue queue
#SBATCH --mem=0 #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-00:55:00 # 
#sbatch --ntasks=56
#SBATCH --ntasks-per-core=1 
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/slurm/tests/test_%x.%j.%a.out    # standard output will be redirected to this file
#SBATCH --job-name=hpl_autotuning_test    # this is your job’s name
#SBATCH --mail-user=tnguyen668@ucmerced.edu
#SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL

source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate
pytest /home/tnguyen668/software/HPL-Scripts/autotuning/tests/

#Run only HPL
#cd /home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles
#mpirun -np 112 ./xhpl


# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


