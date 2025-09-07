from math import sqrt
from pathlib import Path
import os
import struct
import psutil
HPL_EXEC_FOLDER_PATH : Path= Path("/home/tnguyen668/software/hpl-portable/hpl-2.3/bin/pinnacles")
RESULTS_PATH= Path(__file__).parent.joinpath("results")

NUM_PROCESS=1

if "SLURM_JOB_ID" in os.environ: 
    NUM_PROCESS = int(os.environ.get("SLURM_NPROCS", psutil.cpu_count(logical=False)))
    if (NUM_PROCESS < 1):
        raise RuntimeError("SLURM_NTASKS environment variable not found or invalid.")


_availableMemory = int(os.getenv("HPL_RUNNER_MEM", psutil.virtual_memory().available))
# Formula from https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/
MAXIMUM_HPL_N = sqrt(_availableMemory/struct.calcsize("d"))      