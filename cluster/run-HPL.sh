#!/bin/bash
#SBATCH --nodes=1    # request only 1 node
#SBATCH --partition medium      # this job will be submitted to short queue queue
#SBATCH --mem=256000MB #this job is asked for 96G of total memory, use 0 if you want to use entire node memory
#SBATCH --time=0-20:00:00 # 
#SBATCH --ntasks=56
#SBATCH --ntasks-per-core=1
#SBATCH --output=/home/tnguyen668/software/HPL-Scripts/cluster/outputs/hpl_result.%x.%j.out    # standard output will be redirected to this file
#SBATCH --job-name=hpl_run    # this is your job’s name
#SBATCH --mail-user=tnguyen668@ucmerced.edu
#SBATCH --mail-type=ALL  #uncomment the first two lines if you want to receive     the email notifications
#SBATCH --export=ALL
#https://www.netlib.org/benchmark/hpl/tuning.html
#https://www.mgaillard.fr/2022/08/27/benchmark-with-hpl.html


Script_Dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

HPL_TEMPLATE_PATH=$Script_Dir/templates/hpl_template.dat
HPL_DAT_PATH=/home/tiep_nguyen/HPL-Folder/hpl-2.3/bin/pinnacles/HPL.dat
XHPL_PATH=/home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles/xhpl
XHPL_FOLDER=/home/tiep_nguyen/HPL-Folder/hpl-2.3/bin/pinnacles

source "$Script_Dir/setpath.sh"

# default values 
OUTPUT_NAME=output.log # output file name (if any)
DEVICE_OUT=6         #  device out (6=stdout,7=stderr,file)
PROBLEM_SIZE=1            # of problems sizes (N)
N_ARRAY= "178885"
NB_COUNT=4    
NB_ARRAY="40 120 200 280"    
PMAP_MAPPING=0     
N_PROCESS_GRID=1  # Number of process grids (P x Q)   
P_ARRAY="8"    
Q_ARRAY="7"       
THRESHOLD=16.0 # double       
N_PFACT=1        
PFACT_ARRAY="1"       
N_RECURSIVE_CRIT=2       
NBMIN_ARRAY="4 8"         
N_PANEL_RECUR=1           
NDIVS=2           
N_RFACTS=1      
RFACT_ARRAY="2"  #0=left, 1=Crout, 2=Right
BCASTS=6 #
BCAST_ARRAY="0 1 2 3 4 5" #  0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM   
LOOKAHEAD_DEPTH=2  
N_DEPTHS="0 1"          
SWAP_TYPE=2 #   (0=bin-exch,1=long,2=mix)        
SWAP_THRESHOLD=64   
L1_FORM=0   
U_FORM=0
EQUILIBRATION=1   # 0=no,1=yes       
MEM_ALIGN_DBL=8             




# writes to output
sed -e 's%@OUTPUT_NAME@%'"$OUTPUT_NAME"'%' \
    -e 's%@DEVICE_OUT@%'"$DEVICE_OUT"'%' \
    -e 's%@PROBLEM_SIZE@%'"$PROBLEM_SIZE"'%' \
    -e 's%@N_ARRAY@%'"$N_ARRAY"'%' \
    -e 's%@NB_COUNT@%'"$NB_COUNT"'%' \
    -e 's%@NB_ARRAY@%'"$NB_ARRAY"'%' \
    -e 's%@PMAP_MAPPING@%'"$PMAP_MAPPING"'%' \
    -e 's%@N_PROCESS_GRID@%'"$N_PROCESS_GRID"'%' \
    -e 's%@P_ARRAY@%'"$P_ARRAY"'%' \
    -e 's%@Q_ARRAY@%'"$Q_ARRAY"'%' \
    -e 's%@THRESHOLD@%'"$THRESHOLD"'%' \
    -e 's%@N_PFACT@%'"$N_PFACT"'%' \
    -e 's%@PFACT_ARRAY@%'"$PFACT_ARRAY"'%' \
    -e 's%@N_RECURSIVE_CRIT@%'"$N_RECURSIVE_CRIT"'%' \
    -e 's%@NBMIN_ARRAY@%'"$NBMIN_ARRAY"'%' \
    -e 's%@N_PANEL_RECUR@%'"$N_PANEL_RECUR"'%' \
    -e 's%@NDIVS@%'"$NDIVS"'%' \
    -e 's%@N_RFACTS@%'"$N_RFACTS"'%' \
    -e 's%@RFACT_ARRAY@%'"$RFACT_ARRAY"'%' \
    -e 's%@BCASTS@%'"$BCASTS"'%' \
    -e 's%@BCAST_ARRAY@%'"$BCAST_ARRAY"'%' \
    -e 's%@LOOKAHEAD_DEPTH@%'"$LOOKAHEAD_DEPTH"'%' \
    -e 's%@N_DEPTHS@%'"$N_DEPTHS"'%' \
    -e 's%@SWAP_TYPE@%'"$SWAP_TYPE"'%' \
    -e 's%@SWAP_THRESHOLD@%'"$SWAP_THRESHOLD"'%' \
    -e 's%@L1_FORM@%'"$L1_FORM"'%' \
    -e 's%@U_FORM@%'"$U_FORM"'%' \
    -e 's%@EQUILIBRATION@%'"$EQUILIBRATION"'%' \
    -e 's%@MEM_ALIGN_DBL@%'"$MEM_ALIGN_DBL"'%' \
    "$HPL_TEMPLATE_PATH" > "$HPL_DAT_PATH"

cd $XHPL_FOLDER
mpirun -np 56 ./xhpl > "$Script_Dir/outputs/output.log"