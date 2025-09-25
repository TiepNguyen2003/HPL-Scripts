#!/bin/bash
#SBATCH --nodes=1    # request only 1 node
#SBATCH --partition medium      # this job will be submitted to short queue queue

#SBATCH --mem=256000MB #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-20:00:00 # 
#SBATCH --ntasks=56
#SBATCH --ntasks-per-core=1
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/baseline_result.%x.%j.out    # standard output will be redirected to this file
#SBATCH --error=/home/tnguyen668/software/HPL-Scripts/autotuning/results/baseline_result.%x.%j.err

#SBATCH --job-name=hpl_baseline    # this is your job’s name
#SBATCH --mail-user=tnguyen668@ucmerced.edu
#SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL
##SBATCH --constraint="icelake"

source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate # put your virtual environment here


export HPL_RUNNER_MEM=256000
export HPL_NUM_PROCESS=56


python3 /home/tnguyen668/software/HPL-Scripts/autotuning/baseline.py


# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


