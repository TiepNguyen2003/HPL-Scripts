from math import sqrt
import struct
import numpy as np
from skopt.plots import plot_gaussian_process
from skopt import gp_minimize, Space
from skopt.space import Real, Integer, Categorical
from pathlib import Path
import os
import sys
sys.path.append(str(Path(__file__).parent.joinpath("src/HPLWrapper").resolve()))

from HPLConfig import HPLConfig
from HPLRunner import HPLRunner
import pandas as pd
from skopt.plots import plot_convergence
import psutil


hplRunner = HPLRunner()



RESULTS_FOLDER = Path(__file__).parent.joinpath("results")

availableMemory = int(os.getenv("HPL_RUNNER_MEM", psutil.virtual_memory().available))
# Formula from https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/
FullN = sqrt(availableMemory/struct.calcsize("d")) 
space= Space([
    Integer(0.6*FullN,0.8*FullN, name="N"),
    Integer(16,300, name="NB"), # recommended to be 256
    Integer(1,hplRunner.numProcess, name="P")
])
trials = 1
def objectiveFunction(params):
    global trials

    NCoef = int(params[0]/params[1]) # makes sure N array is a multiple of NB array
    print("NCoef " + str(NCoef))
    config = HPLConfig(
        N_Array=[NCoef*params[1]],
        NB_Array=[params[1]],
        P_Array=[8],
        Q_Array=[7],
        PFact_Array=[0, 1, 2],
        NBMin_Array=[1, 2],
        NDIV_Array=[2],
        RFact_Array=[0, 1, 2],
        BCAST_Array=[0],
        Depth_Array=[0],
    )
    print(params[0], params[1])
    hplRunner.setconfig(config)
    results : pd.DataFrame = hplRunner.runHPL()
    trials += 1  

    if results is None:
        return 1000 # large integer
    else: 
        results.to_csv(RESULTS_FOLDER.joinpath("trial_"+str(trials)), index=False)
        return results['Gflops'].max() * -1


result= gp_minimize(objectiveFunction, space, n_calls=10, random_state=0)
print(result)

