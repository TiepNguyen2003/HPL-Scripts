from math import sqrt
from pathlib import Path
import os
import struct
import psutil
HPL_EXEC_FOLDER_PATH : Path= Path("/home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles")
RESULTS_PATH= Path(__file__).parent.joinpath("results")

NUM_PROCESS=int(os.getenv("HPL_NUM_PROCESS", 1))

_availableMemory = int(os.getenv("HPL_RUNNER_MEM", "10000")) # memory in mb
# Formula from https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/
MAXIMUM_HPL_N = sqrt(_availableMemory/struct.calcsize("d"))      
