#!/bin/bash
#SBATCH --nodes=1    # request only 1 node
#SBATCH --partition test      # this job will be submitted to test queue
#SBATCH --mem=96G #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-00:15:00 # 15 minute
#SBATCH --ntasks-per-node=40 # 
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/autotuning/results/test_result.txt    # standard output will be redirected to this file
#SBATCH --job-name=hpl_autotuning_test    # this is your job’s name
##SBATCH --mail-user=tnguyen668
##SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL

source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
source /home/tnguyen668/software/HPL-Scripts/autotuning/.venv/bin/activate # put your virtual environment here
pytest /home/tnguyen668/software/HPL-Scripts/autotuning/tests/test_HPLRunner.py -s
# Please avoid using the ampersand (&) with "srun" if you intend to run processes in the background.


