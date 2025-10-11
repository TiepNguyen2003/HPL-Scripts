import struct
import sys
from pathlib import Path
import os
print(Path(__file__).parent.parent.parent.resolve())
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))
from config import HPL_EXEC_FOLDER_PATH, RESULTS_PATH, NUM_PROCESS, MAXIMUM_HPL_N

import tempfile
from logging import config
from typing import List, Optional
import psutil
from HPLConfig import HPLConfig
from pathlib import Path
import pandas as pd
from HPLResultReader import process_hpl_output
import subprocess
from datetime import datetime
from SLURMConfig import SLURMConfig
import time


HPL_PARAMETER_TEMPLATE = Path(__file__).parent.parent.parent.joinpath("templates","hpl_template.dat")
HPL_EXEC_PATH = HPL_EXEC_FOLDER_PATH.joinpath("xhpl")
SLURM_TEMPLATE = Path(__file__).parent.parent.parent.joinpath("templates","slurm_template.sh")


class HPLRunner:
    config:HPLConfig = None
    numProcess : int = NUM_PROCESS
    _currentLogCount:int # the current new log
    
    _iterator_path : Path
    _MAXIMUM_HPL_N = MAXIMUM_HPL_N
    @property
    def log_folder(self) -> Path:
        """Getter for log_folder"""
        return self._log_folder

    @log_folder.setter
    def log_folder(self, value: Path):
        """Setter for log_folder"""
        if not isinstance(value, Path):
            raise TypeError("log_folder must be a pathlib.Path")
        self._log_folder = value
        self._iterator_path = self._log_folder.joinpath("count")
        try:
            with open(self._iterator_path, 'r') as file:
                content = (file.read().strip())
                print(f"Read iterator file, content is on count '{content}'")
                self._currentLogCount = int(content)
        except (FileNotFoundError, ValueError):
            self._currentLogCount = 0

    @property
    def csv_folder(self) -> Path:
        """Getter for csv_folder"""
        return self._csv_folder

    @csv_folder.setter
    def csv_folder(self, value: Path):
        """Setter for csv_folder"""
        if not isinstance(value, Path):
            raise TypeError("csv_folder must be a pathlib.Path")
        self._csv_folder = value



    def __init__(self):
        # create folders
        RESULTS_PATH.joinpath("dataframes").mkdir(parents=True, exist_ok=True)
        RESULTS_PATH.joinpath("logs").mkdir(parents=True, exist_ok=True)
         
        self.log_folder = RESULTS_PATH.joinpath("logs")
        self.csv_folder = RESULTS_PATH.joinpath("dataframes")
        

    '''
    Runs HPL benchmark. Returns the list of Gflops from execution
    Returns None on failure
    '''
    def runHPL(self) -> Optional[pd.DataFrame]:
        # Sanity Checks (Ensures the partition is runnable)

        for n in self.config.N_Array:
            if n <= 0:
                print(f"Invalid problem size: {n}")
                return None
            
            if (n > self._MAXIMUM_HPL_N):
                print(f"Problem size too large!")
                return None
        for p in self.config.P_Array:
            for q in self.config.Q_Array:
                if p * q > self.numProcess:
                    print(f"Warning, Process grid {p}x{q} exceeds available processes {self.numProcess}")
        try:
            with open(self._iterator_path, 'r') as file:
                content = (file.read().strip())
                self._currentLogCount = int(content)
        except (FileNotFoundError, ValueError):
            self._currentLogCount = 0

           
        # Run HPL
        print("the commandline is {}".format(['srun', '-np', str(self.numProcess), './xhpl']))
        try:
            result_content = subprocess.run(
                ['srun', './xhpl'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=HPL_EXEC_FOLDER_PATH
            )
            with open(self._iterator_path, 'w') as file:
                self._currentLogCount+=1
                file.write(str(self._currentLogCount))  
            result_path = self.log_folder.joinpath(f"hpl_output_{self._currentLogCount}.log")
            dataframe_path = self.csv_folder.joinpath(f"hpl_output_{self._currentLogCount}.csv")
            #print(result_path.resolve())
            print(result_content.stdout)
            print(result_content.stderr)
            with open(result_path, 'w') as file:
                file.write(result_content.stdout)
            dataframe : pd.DataFrame = process_hpl_output(Path(result_path))
            # process content
            with open(dataframe_path, 'w') as file:
                file.write(dataframe.to_csv(index=False))

            return dataframe
        except subprocess.CalledProcessError as e:
            print(f"Error during HPL execution: {e.stderr}")

            return None
        


        



    def _list_to_string(self,l : List) -> str:
        return " ".join(map(str, l))
    
    def _listEnum_to_string(self,l : List) -> str:
        l = list(l)

        return " ".join(map(lambda c: str(c.value), l))
    '''
    Sets the config file for HPL
    '''
    def setconfig(self, config : HPLConfig):
        print(config)
        print(self._listEnum_to_string(config.PFact_Array))
        if config.isValid() == False:
            raise ValueError("Invalid HPLConfig: please check your configuration settings.")
        filecontent="temp"

        with open(HPL_PARAMETER_TEMPLATE, 'r') as file:
            filecontent = file.read()
            print("Opened " + str(HPL_PARAMETER_TEMPLATE))


            
            filecontent = filecontent.replace("@OUTPUT_NAME@", config.Output_Name)
            filecontent = filecontent.replace("@DEVICE_OUT@", config.Device_Out)
            filecontent = filecontent.replace("@PROBLEM_SIZE@", str(len(config.N_Array)))
            filecontent = filecontent.replace("@N_ARRAY@", self._list_to_string(config.N_Array)) # * is the unpack operator
            filecontent = filecontent.replace("@NB_COUNT@", str(len(config.NB_Array)))
            filecontent = filecontent.replace("@NB_ARRAY@", self._list_to_string(config.NB_Array))

            filecontent = filecontent.replace("@PMAP_MAPPING@", str(config.PMAP_Process_Mapping.value))
            filecontent = filecontent.replace("@N_PROCESS_GRID@", str(len(config.P_Array)))
            filecontent = filecontent.replace("@P_ARRAY@", self._list_to_string(config.P_Array))
            filecontent = filecontent.replace("@Q_ARRAY@", self._list_to_string(config.Q_Array))
            filecontent = filecontent.replace("@THRESHOLD@", str(config.Threshold))
            filecontent = filecontent.replace("@N_PFACT@", str(len(config.PFact_Array)))
            filecontent = filecontent.replace("@PFACT_ARRAY@", self._listEnum_to_string(config.PFact_Array))
            filecontent = filecontent.replace("@N_RECURSIVE_CRIT@", str(len(config.NBMin_Array)))
            filecontent = filecontent.replace("@NBMIN_ARRAY@", self._list_to_string(config.NBMin_Array))
            filecontent = filecontent.replace("@N_PANEL_RECUR@", str(len(config.NDIV_Array)))
            filecontent = filecontent.replace("@NDIVS@", self._list_to_string(config.NDIV_Array))
            filecontent = filecontent.replace("@N_RFACTS@", str(len(config.RFact_Array)))
            filecontent = filecontent.replace("@RFACT_ARRAY@", self._listEnum_to_string(config.RFact_Array))
            filecontent = filecontent.replace("@BCASTS@", str(len(config.BCAST_Array)))
            filecontent = filecontent.replace("@BCAST_ARRAY@", self._listEnum_to_string(config.BCAST_Array))
            filecontent = filecontent.replace("@LOOKAHEAD_DEPTH@", str(len(config.Depth_Array)))
            filecontent = filecontent.replace("@N_DEPTHS@", self._list_to_string(config.Depth_Array))
            filecontent = filecontent.replace("@SWAP_TYPE@", str(config.Swap_Type.value))
            filecontent = filecontent.replace("@SWAP_THRESHOLD@", str(config.Swap_Threshold))
            filecontent = filecontent.replace("@L1_FORM@", str(config.L1_Form))
            filecontent = filecontent.replace("@U_FORM@", str(config.U_Form))
            filecontent = filecontent.replace("@EQUILIBRATION@", "1" if config.Equilibration_Enabled == True else "0")
            filecontent = filecontent.replace("@MEM_ALIGN_DBL@", str(config.MemoryAlignment))

            file.close()
            self.config = config
        with open(HPL_EXEC_FOLDER_PATH.joinpath("HPL.dat"), 'w') as file:
            file.write(filecontent)
   