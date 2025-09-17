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

optimizer_path = WRITE_FOLDER.joinpath('optimizer.pk1')
processed_file_path = WRITE_FOLDER.joinpath('processed_files.json')


processed_files = []

runner : HPLRunner
optimizer : HPLOptimizer
iterations = 1
if __name__ == "__main__":
    print("Reading data") 
    print(f"Memory MB {_availableMemory}")
    print(f"bounds are {int(0.2*MAXIMUM_HPL_N)}  {int(MAXIMUM_HPL_N*0.85)}")
    print(f"Numprocess {NUM_PROCESS}")
    try:
        with open(optimizer_path, 'rb') as file:
            optimizer=pickle.load(file)
    except FileNotFoundError:
        optimizer = HPLOptimizer()
        
    try:
        with open(processed_file_path, "rb") as file:
            processed_files_str = json.load(file)

            processed_files = [Path(p) for p in processed_files_str] 
    except FileNotFoundError:
        processed_files=[]
    print(optimizer.optimizer.space)
    print("Creating runner")
    runner = HPLRunner()
    runner.csv_folder=DATAFRAME_FOLDER
    runner.log_folder=LOG_FOLDER

    for i in range(iterations): 
        print("Reading through paths")
        for path in DATAFRAME_FOLDER.iterdir():
            if path.is_file() and (path not in processed_files):
                if (path.suffix != ".csv"):
                    raise ValueError(f"{path} not .csv")
                print(f"Processing {path}" )
                df = process_hpl_csv(path)
                optimizer.tell_runs_dataframe(df)
                processed_files.append(path)

        print("Predicting config")
        next_config : HPLConfig = optimizer.ask_next()
        runner.setconfig(next_config)

        print("Running config")
        runner.runHPL()

        print("Reading through dataframe foldier again")
        for path in DATAFRAME_FOLDER.iterdir():
            if path.is_file() and (path not in processed_files):
                if (path.suffix != ".csv"):
                    raise ValueError(f"{path} not .csv")
                df = process_hpl_csv(path)
                optimizer.tell_runs_dataframe(df)
                processed_files.append(path)

        print("Writing model to disk")
        print(len(processed_files))
        with open(optimizer_path, 'wb') as file:
            pickle.dump(optimizer, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(processed_file_path, 'w') as file:
            processed_files_str = [str(p) for p in processed_files]
            json.dump(processed_files_str, file)
        









