#!/bin/bash
#SBATCH --nodes=1    # request only 1 node
#SBATCH --partition short      # this job will be submitted to short queue queue

#SBATCH --mem=256000MB #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-05:55:00 # 
#SBATCH --ntasks=56
#SBATCH --ntasks-per-core=1
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/hpl_result.%x.%j.out    # standard output will be redirected to this file
#SBATCH --job-name=hpl_autotuning_train    # this is your job’s name
#SBATCH --mail-user=tnguyen668@ucmerced.edu
#SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL
##SBATCH --constraint="sapphire-rapids"

source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate # put your virtual environment here


export HPL_RUNNER_MEM=256000
export HPL_NUM_PROCESS=56

# tests

python3 /home/tnguyen668/software/HPL-Scripts/autotuning/optimize.py


# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


