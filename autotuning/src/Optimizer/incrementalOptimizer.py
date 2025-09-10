from pathlib import Path
import pickle
import string
from typing import List
from HPLOptimizer import HPLOptimizer
from HPLRunner import HPLRunner
from HPLResultReader import get_hpl_runs
from HPLConfig import HPLConfig, HPL_Run
import json
WRITE_FOLDER = Path(__file__).parent.joinpath("cache")



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
                    self.optimizer = HPLOptimizer()
        except:
            self.optimizer = HPLOptimizer()
        self.hplrunner = HPLRunner()
        self._serialize()

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
        for run in runs:
            self.optimizer.tell_run(run)

        self.filesRead.append(str(path))
        self._serialize()
    ''' Sets the next config of HPLRunner'''
    def set_next_config(self):
        config : HPLConfig = self.optimizer.ask_next()

        self.hplrunner.setconfig(config)

    '''Resets the memory to the default state'''
    def reset(self):
        self.optimizer= HPLOptimizer()
        self.filesRead = []
        self._serialize()
        

