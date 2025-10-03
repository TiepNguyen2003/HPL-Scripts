from math import sqrt
from pathlib import Path
import os
import struct
import psutil
from dotenv import load_dotenv

load_dotenv()

HPL_EXEC_FOLDER_PATH : Path= Path("/home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles")
RESULTS_PATH= Path(__file__).parent.joinpath("results")

NUM_PROCESS=int(os.getenv("HPL_NUM_PROCESS", 56))


_availableMemory = int(os.getenv("HPL_RUNNER_MEM", "256000")) # memory in mb
# Formula from https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/

MAXIMUM_HPL_N = int(sqrt(_availableMemory*1048576/struct.calcsize("d")))      
MIN_SPACE_N = int(os.getenv("HPL_MIN_SPACE_N",MAXIMUM_HPL_N * 0.25))
MAX_SPACE_N = int(os.getenv("HPL_MAX_SPACE_N",MAXIMUM_HPL_N * 0.85))

JOB_NAME = str(os.getenv("HPL_JOB_NAME", "hpl_autotuning_train"))

RANK = int(os.getenv("HPL_RANK",1)) - 1 # we subtract by one bc task id starts at 1
NUM_NODES = int(os.getenv("HPL_NUM_NODES",4))
