from logging import config
from typing import List
from config import HPL_EXEC_FOLDER_PATH
from HPLConfig import HPLConfig
from pathlib import Path
import pandas as pd
from HPLResultReader import process_hpl_output
import subprocess

HPL_PARAMETER_TEMPLATE = Path(__file__).parent.joinpath("templates","hpl_template.dat")
HPL_EXEC_PATH = HPL_EXEC_FOLDER_PATH.joinpath("xhpl")
HPL_RESULT_FOLDER = Path(__file__).parent.joinpath("results")

class HPLRunner:
    config:HPLConfig = None
    

    '''
    Runs HPL benchmark. Returns the list of Gflops from execution
    '''
    def runHPL(self) -> pd.DataFrame:
        result_path= str(HPL_RESULT_FOLDER.joinpath("hpl_output.log"))
        #print(HPL_EXEC_PATH.resolve() + "|>" + result_path)
        print(HPL_EXEC_PATH.resolve())
        result_content = subprocess.run(
            ["./xhpl"], cwd=HPL_EXEC_FOLDER_PATH, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        print("Content stdout")
        print(result_content.stdout)
        HPL_RESULT_FOLDER.mkdir(parents=True, exist_ok=True)
        with open(result_path, 'w') as file:
            file.write(result_content.stdout)

        dataframe : pd.DataFrame = process_hpl_output(Path(result_path))

        # process content

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

            