#!/bin/bash
#SBATCH --nodes=1    # request nodes
#SBATCH --partition medium      # this job will be submitted to short queue queue
#SBATCH --exclusive
#SBATCH --mem=256000MB #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-20:00:00 # 
#SBATCH --ntasks=56
#SBATCH --ntasks-per-core=1
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/slurm/test_%x.%j.%a.out    # standard output will be redirected to this file
#SBATCH --job-name=hpl_autotuning_train    # this is your job’s name
#SBATCH --mail-user=tnguyen668@ucmerced.edu
#SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL
##SBATCH --constraint="sapphire-rapids"


source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate # put your virtual environment here


export HPL_RUNNER_MEM=256000
export HPL_NUM_PROCESS=56

export HPL_MAX_SPACE_N=1000
export HPL_MIN_SPACE_N=200

#export HPL_RANK=${SLURM_ARRAY_TASK_ID}
export HPL_NUM_NODES=4

# tests

python3 /home/tnguyen668/software/HPL-Scripts/autotuning/optimize.py


# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


