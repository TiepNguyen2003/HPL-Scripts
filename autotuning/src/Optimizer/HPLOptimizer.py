import numpy as np

from skopt import Optimizer
from skopt.space import Real, Integer, Categorical, Space

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.resolve())) 

from config import MAXIMUM_HPL_N, NUM_PROCESS
from HPLConfig import HPLConfig, HPL_Run, PMapEnum, BCastEnum, PFactEnum, RFactEnum



hpl_config_space = Space([
    Integer(MAXIMUM_HPL_N*0.6,MAXIMUM_HPL_N*0.9, name="N"),
    Integer(1,300, name="NB"), # recommended to be 256
    Integer(0, NUM_PROCESS,name="P"),
    Integer(0, NUM_PROCESS,name="Q"),
    Categorical(list(PMapEnum), name="PMap"),
    Categorical(list(PFactEnum), name="PFact"),
    Categorical(list(RFactEnum), name="RFact"),
    Categorical(list(BCastEnum), name="BCast"),
    Integer(0, 5, name="Depth"),
    Categorical([0,1], name="L1"),
    Categorical([0,1], name="U"),
    Categorical([0,1], name="Equilibration_Enabled")
])

class HPLOptimizer:
    optimizer : Optimizer

    def __init__(self):
        self.optimizer = Optimizer(
            dimensions=hpl_config_space.dimensions,
            base_estimator="GP",
            acq_func="LCB",
            acq_optimizer="auto",
            n_initial_points=10,
            random_state=42
        )
    def tell_run(self, run : HPL_Run):
        #TODO, add flexibility so that variables can easily be removed from space
        x = [run.N, 
             run.NB, 
             run.P, 
             run.Q, 
             run.PMAP_Process_Mapping,
             run.PFact,
             run.RFact,
             run.BCast,
             run.Depth,
             run.L1,
             run.U,
             int(run.Equilibration_Enabled)]
        
        print(x)
        self.optimizer.tell(x, run.Gflops)
    
    def ask_next(self) -> HPLConfig:
        x = self.optimizer.ask()
        # convert x to a dictionary
        param_dict = {dim.name: val for dim, val in zip(hpl_config_space.dimensions, x)}

        param_dict['Q'] = int(NUM_PROCESS / param_dict['P'])
        # sanity checks
        if (param_dict['P'] == 0 or param_dict['Q'] == 0):
            param_dict['P'] = 1
            param_dict['Q'] = 1
        #
        if (param_dict['N'] < param_dict['NB']):
            param_dict['NB'] = param_dict['N']

        hpl_config = HPLConfig(
            N_Array=[param_dict['N']],
            NB_Array=[param_dict['NB']],
            P_Array=[param_dict['P']],
            Q_Array=[],
            PMAP_Process_Mapping=param_dict['PMap'],
            PFact_Array=[param_dict['PFact']],
            RFact_Array=[param_dict['RFact']],
            BCAST_Array=[param_dict['BCast']],
            Depth_Array=[param_dict['Depth']],
            L1_Form=param_dict['L1'],
            U_Form=param_dict['U'],
            Equilibration_Enabled=bool(param_dict['Equilibration_Enabled'])
        )

        return hpl_config