#!/bin/bash

Install_Path="$HOME/HPL-Folder"
Build_Process_Count=8

OPENMPI_URL="https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.8.tar.gz"
BLAS_URL="https://github.com/OpenMathLib/OpenBLAS/releases/download/v0.3.30/OpenBLAS-0.3.30.tar.gz"
HPL_URL=https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz

MPI_Folder=mpi-install
OpenBLAS_Folder=openblas-install

HPL_PATH="$Install_Path"/hpl-2.3
MPI_PATH="$Install_Path"/"$MPI_Folder"
OpenBLAS_Path="$Install_Path"/"$OpenBLAS_Folder" # Path of the OpenBLAS install

