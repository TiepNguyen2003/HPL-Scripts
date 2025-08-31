from math import sqrt
import struct
import numpy as np
from skopt.plots import plot_gaussian_process
from skopt import gp_minimize, Space
from skopt.space import Real, Integer, Categorical
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.joinpath("src/HPLWrapper").resolve()))

from HPLConfig import HPLConfig
from HPLRunner import HPLRunner
import pandas as pd
from skopt.plots import plot_convergence
import psutil


hplRunner = HPLRunner()



RESULTS_FOLDER = Path(__file__).parent.joinpath("results")

availableMemory = psutil.virtual_memory().available
# Formula from https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/
NRatio = sqrt(availableMemory/struct.calcsize("d")) 
space= Space([
    Integer(0.2*NRatio,0.4*NRatio, name="N"),
    Integer(16,300, name="NB"), # recommended to be 256
    Integer(1,hplRunner.numProcess, name="P")
])
trials = 1
def objectiveFunction(params):
    global trials
    config = HPLConfig(
        N_Array=[params[0]],
        NB_Array=[params[1]],
        P_Array=[4],
        Q_Array=[2],
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

    results.to_csv(RESULTS_FOLDER.joinpath("trial_"+str(trials)), index=False)
    trials += 1  

    return results['Gflops'].max() * -1


result= gp_minimize(objectiveFunction, space, n_calls=30, random_state=0)
print(result)

