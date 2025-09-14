import numpy as np

from skopt import Optimizer
from skopt.space import Real, Integer, Categorical, Space

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.resolve())) 

from config import MAXIMUM_HPL_N, NUM_PROCESS
from HPLConfig import HPLConfig, HPL_Run, PMapEnum, BCastEnum, PFactEnum, RFactEnum
from typing import List
import pandas as pd



hpl_config_space = Space([
    Integer(0.5*MAXIMUM_HPL_N,MAXIMUM_HPL_N*0.8, name="N"),
    Integer(1,300, name="NB"), # recommended to be 256
    Integer(0, NUM_PROCESS,name="P"),
    Integer(0, NUM_PROCESS,name="Q"),
    #Categorical(list(PMapEnum), name="PMap"),
    Categorical(list(PFactEnum), name="PFact"),
    Categorical(list(RFactEnum), name="RFact"),
    Categorical(list(BCastEnum), name="BCast"),
    Integer(1, 20, name="NBMin"),
    Integer(2, 20, name = "NbDiv"),
    Integer(0, 5, name="Depth"),
    #Categorical([0,1], name="L1"),
    #Categorical([0,1], name="U"),
    #Categorical([0,1], name="Equilibration_Enabled")
])

class HPLOptimizer:
    optimizer : Optimizer
    runs_per_ask : int = 2 # how many runs per ask it should ask
    
    
    def __init__(self):
        self.optimizer = Optimizer(
            dimensions=hpl_config_space.dimensions,
            base_estimator="GP",
            acq_func="LCB",
            acq_optimizer="auto",
            n_initial_points=10,
            random_state=42
        )
    def get_run_count(self):
        return len(self.optimizer.Xi)

    def tell_run(self, run : HPL_Run):
        #TODO, add flexibility so that variables can easily be removed from space
        x = [run.N, 
            run.NB, 
            run.P, 
            run.Q,
            run.PFact,
            run.RFact,
            run.BCast,
            run.Nbmin,
            run.Nbdiv,
            run.Depth
            ]
        self.optimizer.tell(x, run.Gflops)

    def tell_runs(self, runs : List[HPL_Run]):
        #TODO, add flexibility so that variables can easily be removed from space
        x = [[r.N, r.NB, r.P, r.Q, r.PFact, r.RFact, r.BCast, r.Nbmin, r.Nbdiv, r.Depth] for r in runs]

        gflops : List[float] = list(map(lambda c: -1 * c.Gflops, runs)) # maximize Gflops by minimizing -Gflops


        
        self.optimizer.tell(x, gflops)
    
    def tell_runs_dataframe(self, df : pd.DataFrame):
        required_columns = {'N',
                            'NB',
                            'P',
                            'Q',
                            'BCast',
                            'PFact',
                            'RFact',
                            'Nbmin',
                            'Nbdiv',
                            'Depth',
                            'Gflops',
                            'passed'}
        
        if required_columns.issubset(df.columns) == False:
            raise ValueError("DF does not contain columns")
        
        filtered_df = df[df['passed'] == True]

        X = filtered_df[["N","NB", "P", "Q", "PFact", "RFact", "BCast", "Nbmin", "Nbdiv", "Depth"]].values.tolist()

        for r in X:
            try:
                transform_r = hpl_config_space.transform(r)
            except:
                print(r)
                print("Failed")
        Y = (filtered_df['Gflops'].values * -1).tolist()
        self.optimizer.tell(X,Y)




    def ask_next(self) -> HPLConfig:        
        '''
        hpl_config = HPLConfig(
            N_Array=[param_dict['N']],
            NB_Array=[param_dict['NB']],
            P_Array=[param_dict['P']],
            Q_Array=[param_dict['Q']],
            PMAP_Process_Mapping=param_dict['PMap'],
            PFact_Array=[param_dict['PFact']],
            RFact_Array=[param_dict['RFact']],
            BCAST_Array=[param_dict['BCast']],
            Depth_Array=[param_dict['Depth']],
            NBMin_Array=[param_dict['NBMin']],
            NDIV_Array=[param_dict['NDiv']],
            L1_Form=param_dict['L1'],
            U_Form=param_dict['U'],
            Equilibration_Enabled=bool(param_dict['Equilibration_Enabled'])
        )
        '''

        _N_Array = []
        _NB_Array = []
        _P_Array = []
        _Q_Array = []
        _PFact_Array = set()
        _RFact_Array = set()
        _BCAST_Array = set()
        _Depth_Array = []
        _NBMin_Array = []
        _NDIV_Array = []

        for i in range(self.runs_per_ask):
            x = self.optimizer.ask()
            # convert x to a dictionary
            param_dict = {dim.name: val for dim, val in zip(hpl_config_space.dimensions, x)}

            if (param_dict['P'] == 0):
                param_dict['P'] = 1
            #
            param_dict['Q'] = (int(NUM_PROCESS / int(param_dict['P'])))
            # sanity checks
            
            if (int(param_dict['N']) < int(param_dict['NB'])):
                param_dict['NB'] = param_dict['N']

            _N_Array.append(param_dict['N'])
            _NB_Array.append(param_dict['NB'])
            _P_Array.append(param_dict['P'])
            _Q_Array.append(param_dict['Q'])
            _PFact_Array.add(param_dict['PFact'])
            _RFact_Array.add(param_dict['RFact'])
            _Depth_Array.append(param_dict['Depth'])
            _NBMin_Array.append(param_dict['NBMin'])
            _NDIV_Array.append(param_dict['NbDiv'])
            _BCAST_Array.add(param_dict['BCast'])
        hpl_config = HPLConfig(
            N_Array=_N_Array,
            NB_Array=_NB_Array,
            P_Array=_P_Array,
            Q_Array=_Q_Array,
            PFact_Array=_PFact_Array,
            RFact_Array=_RFact_Array,
            BCAST_Array=_BCAST_Array,
            Depth_Array=_Depth_Array,
            NBMin_Array=_NBMin_Array,
            NDIV_Array=_NDIV_Array,
            L1_Form=0,
            U_Form=0,
            Equilibration_Enabled=1
        )

        return hpl_config