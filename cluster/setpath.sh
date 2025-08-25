#!/bin/bash

Script_Dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "$Script_Dir/config.sh"

export LD_LIBRARY_PATH="$Install_Path/$MPI_Folder/lib/:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$Install_Path/$OpenBLAS_Folder/lib/:$LD_LIBRARY_PATH"
export PATH="$Install_Path/$MPI_Folder/bin:$PATH"
export PATH="$Install_Path/$OpenBLAS_Folder/bin:$PATH"
