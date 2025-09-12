from pathlib import Path
import pickle
import string
from typing import List
from HPLOptimizer import HPLOptimizer
from HPLRunner import HPLRunner
from HPLResultReader import get_hpl_runs
from HPLConfig import HPLConfig, HPL_Run
import json
import os
WRITE_FOLDER = Path(__file__).parent.joinpath("cache")
WRITE_FOLDER.mkdir(parents=True, exist_ok=True)


default_config = HPLConfig(
    N_Array=[29,30,34,35],
    NB_Array=[1,2,3,4],
    P_Array=[2,1,4],
    Q_Array=[2,4,1],
    PFact_Array=[0,1,2],
    RFact_Array=[0,1,2],
    BCAST_Array=[0],
    Depth_Array=[0],
    NBMin_Array=[2,4],
    NDIV_Array=[2],
    L1_Form=0,
    U_Form=0,
    Equilibration_Enabled=1
)

class IncrementalOptimizer():
    filesRead : List[str]
    optimizer: HPLOptimizer
    hplrunner: HPLRunner
    def __init__(self):
        
        try:
            with open(WRITE_FOLDER.joinpath("filesread.json"), "r") as f:
                self.filesRead = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.filesRead = []

        try:
            with open(WRITE_FOLDER.joinpath("optimizer.pk1"), "r") as f:
                self.optimizer = pickle.load(f)
                if (self.optimizer is None):
                    print("Creating new optimizer after reading")
                    self.optimizer = HPLOptimizer()
        except Exception as e:
            print("Exception:", e)
            print("Failed to read, creating new optimizer")
            self.optimizer = HPLOptimizer()
        
        print(self.optimizer)
        self.hplrunner = HPLRunner()
        print(self.optimizer.get_run_count())

    def _serialize(self):
        with open(WRITE_FOLDER.joinpath("filesread.json"), "w") as f:  # 'w' = text mode
            json.dump(self.filesRead, f, indent=2)  # indent=2 makes it readable

    
        with open(WRITE_FOLDER.joinpath("optimizer.pk1"), "wb") as f:
            pickle.dump(self.optimizer, f)
    
    '''Adds a file to the training data'''
    def process_file(self, path : Path):
        if str(path) in self.filesRead:
            print("Ignoring path {path} as we already contain it")
            return

        runs : List[HPL_Run] = get_hpl_runs(path)
        gflops : List[float] = list(map(lambda c: -1 * c.Gflops, runs)) # we want to maximize gflops but ourfunction is a minimizer
        
        self.optimizer.tell_runs(runs)

        self.filesRead.append(str(path))
        self._serialize()
    ''' Sets the next config of HPLRunner'''
    def set_next_config(self):
        config : HPLConfig 

        #if len(self.filesRead) > 0:
            
        #else:
        #    config = default_config
        config = self.optimizer.ask_next()
        self.hplrunner.setconfig(config)

    '''Resets the memory to the default state'''
    def reset(self):
        self.optimizer= HPLOptimizer()
        self.filesRead = []
        self._serialize()
        

