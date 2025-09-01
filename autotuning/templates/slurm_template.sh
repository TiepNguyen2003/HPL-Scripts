#!/bin/bash
#SBATCH --nodes=@NODES@    # request only 1 node
#SBATCH --partition=@PARTITION@      # this job will be submitted to test queue
#SBATCH --mem=@ALLOC_GB@ #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=@TIME@ # 
#SBATCH --ntasks-per-node=@NTASKS_PERNODE@ # 
#SBATCH --output=@OUTPUT_FILE@    # standard output will be redirected to this file
#SBATCH --job-name=@JOB_NAME@    # this is your job’s name
##SBATCH --mail-user=@MAIL_USER@
##SBATCH --mail-type=@MAIL_TYPE@  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL

set HPL_RUNNER_MEM=@ALLOC_MB@

source /home/tnguyen668/software/HPL-Scripts/cluster/setpath.sh
cd /home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles
mpirun -np @NUM_PROCS@ xhpl


