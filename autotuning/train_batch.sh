#!/bin/bash
#SBATCH --nodes=1    # request only 1 node
#SBATCH --partition test      # this job will be submitted to test queue
#SBATCH --mem=20000M #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-00:50:00 # 
#SBATCH --ntasks-per-node=8 # 
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/hpl_result.out    # standard output will be redirected to this file
#SBATCH --job-name=hpl_autotuning_train    # this is your job’s name
##SBATCH --mail-user=tnguyen668
##SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL

set HPL_RUNNER_MEM=20000
set HPL_NUM_PROCESS=8

source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate # put your virtual environment here

# tests
echo $HPL_RUNNER_MEM
python3 /home/tnguyen668/software/HPL-Scripts/autotuning/optimize.py



# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


