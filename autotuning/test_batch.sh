#!/bin/bash
#SBATCH --nodes=1    # request nodes
#SBATCH --partition test      # this job will be submitted to short queue queue
#SBATCH --mem=256000MB #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-00:55:00 # 
#SBATCH --ntasks=56
#SBATCH --ntasks-per-core=1
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/slurm/test_%x.%j.%a.out    # standard output will be redirected to this file
#SBATCH --job-name=hpl_autotuning_test    # this is your job’s name
#SBATCH --mail-user=tnguyen668@ucmerced.edu
#SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL
##SBATCH --constraint="sapphire-rapids"
##SBATCH --array=1-4


source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate # put your virtual environment here
pytest /home/tnguyen668/software/HPL-Scripts/autotuning/tests/ -s


# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


