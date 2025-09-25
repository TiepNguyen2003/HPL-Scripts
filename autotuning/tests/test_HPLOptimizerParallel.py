import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))


sys.path.append(str(Path(__file__).parent.parent.joinpath("src/Optimizer").resolve()))
TEST_SAMPLES_FOLDER = Path(__file__).parent.joinpath("test_samples")


from HPLResultReader import process_hpl_csv
import config
from HPLOptimizer import HPLOptimizer
from skopt import Optimizer
from skopt.space import Real, Integer, Categorical, Space
from HPLConfig import HPLConfig, HPL_Run, PFactEnum, RFactEnum, BCastEnum, PMapEnum

test_space = Space([
    Integer(1,2000000, name="N"),
    Integer(1,300, name="NB"), # recommended to be 256
    Integer(0, 16,name="P"),
    #Integer(0, 16,name="Q"),
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




def test_request_parallel():
    nodes = 4

    configs = []

    for i in range(nodes):
        
        optimizer = HPLOptimizer()
        optimizer._rank=i
        optimizer.optimizer.space = test_space
        df = process_hpl_csv(TEST_SAMPLES_FOLDER.joinpath('hpl_output.csv'))

        optimizer.tell_runs_dataframe(df)
        con = optimizer.ask_next()
        for val in configs:
            assert con != config, "Duplicate configs created"
        configs.append(con)



