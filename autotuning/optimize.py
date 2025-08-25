import numpy as np
from skopt.plots import plot_gaussian_process
from skopt import gp_minimize, Space
from skopt.space import Real, Integer, Categorical
from HPLConfig import HPLConfig
from HPLRunner import HPLRunner
import pandas as pd
from pathlib import Path
from skopt.plots import plot_convergence



hplRunner = HPLRunner()

RESULTS_FOLDER = Path(__file__).parent.joinpath("results")
space= Space([
    Integer(10,100, name="N"),
    Integer(4,50, name="NB")
])
trials = 1
def objectiveFunction(params):
    global trials
    config = HPLConfig(
        N_Array=[params[0]],
        NB_Array=[params[1]],
        P_Array=[1],
        Q_Array=[1],
        PFact_Array=[0, 1, 2],
        NBMin_Array=[1, 2],
        NDIV_Array=[2],
        RFact_Array=[0, 1, 2],
        BCAST_Array=[0],
        Depth_Array=[0],
    )
    hplRunner.setconfig(config)
    results : pd.DataFrame = hplRunner.runHPL()

    results.to_csv(RESULTS_FOLDER.joinpath("trial_"+str(trials)), index=False)
    trials += 1  

    return results['Gflops'].max() * -1


result= gp_minimize(objectiveFunction, space, n_calls=30, random_state=0)
print(result)

