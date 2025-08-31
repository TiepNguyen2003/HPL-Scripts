import struct
import sys
from pathlib import Path
print(Path(__file__).parent.parent.parent.resolve())
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))
from config import HPL_EXEC_FOLDER_PATH, RESULTS_PATH


from logging import config
from typing import List, Optional
import psutil
from HPLConfig import HPLConfig
from pathlib import Path
import pandas as pd
from HPLResultReader import process_hpl_output
import subprocess
from datetime import datetime

HPL_PARAMETER_TEMPLATE = Path(__file__).parent.parent.parent.joinpath("templates","hpl_template.dat")
HPL_EXEC_PATH = HPL_EXEC_FOLDER_PATH.joinpath("xhpl")

class HPLRunner:
    config:HPLConfig = None
    numProcess: int
    _currentLogCount:int # the current new log
    

    
    _iterator_path = Path(RESULTS_PATH.joinpath("logs","count"))
    def __init__(self):
        self.numProcess = psutil.cpu_count(logical=False)
        
        
        try:
            with open(self._iterator_path, 'r') as file:
                content = (file.read().strip())
                print(f"Read iterator file, content is on count '{content}'")
                self._currentLogCount = int(content)
        except (FileNotFoundError, ValueError):
            self._currentLogCount = 0
        

    '''
    Runs HPL benchmark. Returns the list of Gflops from execution
    Returns None on failure
    '''
    def runHPL(self) -> Optional[pd.DataFrame]:
        # Sanity Checks (Ensures the partition is runnable)

        currentAvailMemory = psutil.virtual_memory().available
        print(currentAvailMemory)
        for n in self.config.N_Array:
            if n <= 0:
                print(f"Invalid problem size: {n}")
                return None
            
            if (n^2 * struct.calcsize("d") > currentAvailMemory):
                print(f"Problem size too large!")
                return None
        for p in self.config.P_Array:
            for q in self.config.Q_Array:
                if p * q > self.numProcess:
                    print(f"Process grid {p}x{q} exceeds available processes {self.numProcess}")
                    return None

        # 
        #print(HPL_EXEC_PATH.resolve() + "|>" + result_path)
        print(HPL_EXEC_PATH.resolve())
        result_content = subprocess.run(
            ['mpirun', '-np', str(self.numProcess), 'xhpl'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=HPL_EXEC_FOLDER_PATH
        )
        print("the commandline is {}".format(result_content.args))


        result_path = RESULTS_PATH.joinpath("logs", f"hpl_output_{self._currentLogCount}.log")
        dataframe_path = RESULTS_PATH.joinpath("dataframes", f"hpl_output_{self._currentLogCount}.csv")
        result_path.parent.mkdir(parents=True, exist_ok=True)
        #print(result_path.resolve())
        print(result_content.stdout)
        print(result_content.stderr)
        with open(result_path, 'w') as file:
            file.write(result_content.stdout)
            self._currentLogCount+=1
        with open(self._iterator_path, 'w') as file:
            file.write(str(self._currentLogCount))

        dataframe : pd.DataFrame = process_hpl_output(Path(result_path))

        # process content

        with open(dataframe_path, 'w') as file:
            file.write(dataframe.to_csv(index=False))

        return dataframe

    def _list_to_string(self,list : List) -> str:
        return " ".join(map(str, list))
    '''
    Sets the config file for HPL
    '''
    def setconfig(self, config : HPLConfig):

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
            filecontent = filecontent.replace("@PMAP_MAPPING@", str(config.PMAP_Process_Mapping))
            filecontent = filecontent.replace("@N_PROCESS_GRID@", str(len(config.P_Array)))
            filecontent = filecontent.replace("@P_ARRAY@", self._list_to_string(config.P_Array))
            filecontent = filecontent.replace("@Q_ARRAY@", self._list_to_string(config.Q_Array))
            filecontent = filecontent.replace("@THRESHOLD@", str(config.Threshold))
            filecontent = filecontent.replace("@N_PFACT@", str(len(config.PFact_Array)))
            filecontent = filecontent.replace("@PFACT_ARRAY@", self._list_to_string(config.PFact_Array))
            filecontent = filecontent.replace("@N_RECURSIVE_CRIT@", str(len(config.NBMin_Array)))
            filecontent = filecontent.replace("@NBMIN_ARRAY@", self._list_to_string(config.NBMin_Array))
            filecontent = filecontent.replace("@N_PANEL_RECUR@", str(len(config.NDIV_Array)))
            filecontent = filecontent.replace("@NDIVS@", self._list_to_string(config.NDIV_Array))
            filecontent = filecontent.replace("@N_RFACTS@", str(len(config.RFact_Array)))
            filecontent = filecontent.replace("@RFACT_ARRAY@", self._list_to_string(config.RFact_Array))
            filecontent = filecontent.replace("@BCASTS@", str(len(config.BCAST_Array)))
            filecontent = filecontent.replace("@BCAST_ARRAY@", self._list_to_string(config.BCAST_Array))
            filecontent = filecontent.replace("@LOOKAHEAD_DEPTH@", str(len(config.Depth_Array)))
            filecontent = filecontent.replace("@N_DEPTHS@", self._list_to_string(config.Depth_Array))
            filecontent = filecontent.replace("@SWAP_TYPE@", str(config.Swap_Type))
            filecontent = filecontent.replace("@SWAP_THRESHOLD@", str(config.Swap_Threshold))
            filecontent = filecontent.replace("@L1_FORM@", str(config.L1_Form))
            filecontent = filecontent.replace("@U_FORM@", str(config.U_Form))
            filecontent = filecontent.replace("@EQUILIBRATION@", "1" if config.Equilibration_Enabled == True else "0")
            filecontent = filecontent.replace("@MEM_ALIGN_DBL@", str(config.MemoryAlignment))

            file.close()
            self.config = config
        with open(HPL_EXEC_FOLDER_PATH.joinpath("HPL.dat"), 'w') as file:
            file.write(filecontent)

            