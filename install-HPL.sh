#!/bin/bash
Script_Dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
Make_Template_Path="$Script_Dir/Make_Template.in"
Config_Path="$Script_Dir/config.sh"
source $Config_Path



# Local Config
Make_Name="local_machine"

Shell=/bin/sh
# shellcheck disable=SC2016
Arch=$Make_Name

TopDir="$Install_Path/hpl-2.3"


MPDir="$MPI_PATH"
MPInc= #-I$"$MPDir"/include
MPLib= #"$MPDir"/lib/libmpi.la

LADir="$OpenBLAS_Path"
LAInc="-I$LADir/include"
LALib="$LADir/lib/libopenblas.so"

F2Defs=

HPL_Opts="-DHPL_DETAILED_TIMING -DHPL_PROGRESS_REPORT"

CC="$Install_Path"/"$MPI_Folder"/bin/mpicc
CCNoOpt= # Includes $(HPL_DEFS)
CCFlags='-O3 -w -z noexecstack -z relro -z now -Wall' # Includes $(HPL_DEFS)

Linker="$Install_Path"/"$MPI_Folder"/bin/mpicc
LinkFlags='$(CCFLAGS) $(OMP_DEFS)'

Archiver=ar
ArFlags=r
RanLib=echo
# Make a copy of make_generic

cd "$Install_Path"/hpl-2.3 || { echo 'Could not go to HPL!' >&2; exit1; }

Make_File=./Make.$Make_Name

touch $Make_File

sed -e 's%@SHELL@%'"$Shell"'%' \
    -e 's%@CD@%cd%' \
    -e 's%@CP@%cp%' \
    -e 's%@LN_S@%ln -s%' \
    -e 's%@MKDIR@%mkdir%' \
    -e 's%@RM@%/bin/rm -f%' \
    -e 's%@TOUCH@%touch%' \
    -e 's%@ARCH@%'"$Arch"'%' \
    -e 's%@CC@%'"$CC"'%' \
    -e 's%@TOPdir@%'"$TopDir"'%' \
    -e 's%@CCNOOPT@%'"$CCNoOpt"'%' \
    -e 's%@CCFLAGS@%'"$CCFlags"'%' \
    -e 's%@LINKER@%'"$Linker"'%' \
    -e 's%@HPL_OPTS@%'"$HPL_Opts"'%'\
    -e 's%@LINKFLAGS@%'"$LinkFlags"'%' \
    -e 's%@ARCHIVER@%'"$Archiver"'%' \
    -e 's%@ARFLAGS@%'"$ArFlags"'%' \
    -e 's%@RANLIB@%'"$RanLib"'%' \
    -e 's%@MPDIR@%'"$MPDir"'%' \
    -e 's%@MPINC@%'"$MPInc"'%' \
    -e 's%@MPLIB@%'"$MPLib"'%' \
    -e 's%@F2CDEFS@%'"$F2Defs"'%' \
    -e 's%@LADIR@%'"$LADir"'%' \
    -e 's%@LAINC@%'"$LAInc"'%' \
    -e 's%@LALIB@%'"$LALib"'%' \
    "$Make_Template_Path" > $Make_File


make arch="$Make_Name" clean
make arch="$Make_Name"



