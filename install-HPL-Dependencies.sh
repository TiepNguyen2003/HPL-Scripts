#!/bin/bash
# Config

# Notes
Script_Dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
Install_Path=dummy;
OpenBLAS_Folder=dummy
MPI_Folder=dummy

source "$Script_Dir/config.sh"
#
cd "$Install_Path" || { mkdir -p "$Install_Path" ; cd "$Install_Path" || { echo || "Cannot make $Install_Path" >&2 ; exit 1;} ;}

mkdir -p "$OpenBLAS_Folder"
mkdir -p "$MPI_Folder"
 
wget "$OPENMPI_URL"|| { echo 'Could not get OpenMPI' >&2; exit 1;} 
wget "$BLAS_URL"|| { echo 'Could not get BLAS' >&2; exit 1;} 
wget "$HPL_URL"|| { echo 'Could not get HPL' >&2; exit 1;} 


tar -xzvf OpenBLAS-0.3.30.tar.gz
tar -xzvf hpl-2.3.tar.gz
tar -xzvf openmpi-5.0.8.tar.gz

# install openmpi

cd "$Install_Path"/openmpi-5.0.8 || { echo 'Could not go to openmp!' >&2; exit 1;} 

./configure --prefix="$Install_Path"/"$MPI_Folder" 2>&1  | tee config.out
make -j"$Build_Process_Count" all 2>&1 | tee make.out
make install 2>&1 | tee install.out


# install openblas

cd "$Install_Path"/OpenBLAS-0.3.30 || { echo 'Could not go to Openblas!' >&2; exit 1;} 

make -j"$Build_Process_Count"
make PREFIX="$Install_Path"/"$OpenBLAS_Folder" install




