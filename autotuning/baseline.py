import sys
from pathlib import Path
import pickle
import json
import pandas as pd

sys.path.append(str(Path(__file__).parent.joinpath("src/HPLWrapper").resolve()))
sys.path.append(str(Path(__file__).parent.joinpath("src/Optimizer").resolve()))

from HPLOptimizer import HPLOptimizer
from HPLConfig import HPLConfig
from HPLResultReader import is_hpl_config, get_hpl_runs, process_hpl_csv
from HPLRunner import HPLRunner
from config import RESULTS_PATH, MAXIMUM_HPL_N, NUM_PROCESS, _availableMemory

model_name = "train_4"

WRITE_FOLDER = RESULTS_PATH.joinpath(model_name)
LOG_FOLDER = WRITE_FOLDER.joinpath("logs")
DATAFRAME_FOLDER = WRITE_FOLDER.joinpath("dataframes")

WRITE_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_FOLDER.mkdir(parents=True, exist_ok=True)
DATAFRAME_FOLDER.mkdir(parents=True, exist_ok=True)


runner : HPLRunner

config : HPLConfig = HPLConfig(
    N_Array=[0.8*MAXIMUM_HPL_N],
    NB_Array=[160,240],
    P_Array=[8],
    Q_Array=[7],
    PFact_Array=[0],
    NBMin_Array=[4, 8],
    NDIV_Array=[2],
    RFact_Array=[0],
    BCAST_Array=[1,3],
    Depth_Array=[0],
)
if __name__ == "__main__":
    print("Performing baseline run") 
    print(f"Memory MB {_availableMemory}")
    print(f"Numprocess {NUM_PROCESS}")
    
    runner = HPLRunner()
    runner.csv_folder=DATAFRAME_FOLDER
    runner.log_folder=LOG_FOLDER

    runner.setconfig(config)

    print("Running config")
    runner.runHPL()
        









