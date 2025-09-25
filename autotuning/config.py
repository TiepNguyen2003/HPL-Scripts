from math import sqrt
from pathlib import Path
import os
import struct
import psutil
from dotenv import load_dotenv

load_dotenv()

HPL_EXEC_FOLDER_PATH : Path= Path("/home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles")
RESULTS_PATH= Path(__file__).parent.joinpath("results")

NUM_PROCESS=int(os.getenv("HPL_NUM_PROCESS", 1))


_availableMemory = int(os.getenv("HPL_RUNNER_MEM", "30000")) # memory in mb
# Formula from https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/

MAXIMUM_HPL_N = int(sqrt(_availableMemory*1000000/struct.calcsize("d")))      
MIN_SPACE_N = os.getenv("HPL_MIN_SPACE_N",int(MAXIMUM_HPL_N * 0.65))
MAX_SPACE_N = os.getenv("HPL_MAX_SPACE_N",int(MAXIMUM_HPL_N * 0.95))

RANK = int(os.getenv("SLURM_ARRAY_TASK_ID",1)) - 1 # we subtract by one bc task id starts at 1
NUM_NODES = int(os.getenv("SLURM_ARRAY_TASK_COUNT",4))
