import sys
from pathlib import Path
from typing import List
import pandas as pd
import pytest
from skopt import Optimizer
from skopt.space import Real, Integer, Categorical, Space


sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLResultReader import process_hpl_output, get_hpl_config, get_hpl_runs,process_hpl_csv
from HPLConfig import HPLConfig, HPL_Run, PFactEnum, RFactEnum, BCastEnum, PMapEnum

sys.path.append(str(Path(__file__).parent.parent.joinpath("src/Optimizer").resolve()))
from HPLOptimizer import HPLOptimizer
HPL_OUTPUT_FILE= Path(__file__).parent.joinpath("test_samples/hpl_output.log")
TEST_SAMPLES_FOLDER = Path(__file__).parent.joinpath("test_samples")



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


hpl_optimizer = HPLOptimizer()
hpl_optimizer.optimizer.space = test_space

def test_tell_run():
    run_list : List[HPL_Run]  = get_hpl_runs(HPL_OUTPUT_FILE)
    for run in run_list:
        hpl_optimizer.tell_run(run)

def test_tell_runs():
    run_list : List[HPL_Run]  = get_hpl_runs(HPL_OUTPUT_FILE)
    hpl_optimizer.tell_runs(run_list)
    
def test_tell_dataframe():
    df = process_hpl_csv(TEST_SAMPLES_FOLDER.joinpath('hpl_output.csv'))

    hpl_optimizer.tell_runs_dataframe(df)

def test_ask():
    config = hpl_optimizer.ask_next()
    print(config)

def test_ask_learn():
    config1 = hpl_optimizer.ask_next()
    run_list : List[HPL_Run]  = get_hpl_runs(HPL_OUTPUT_FILE)
    hpl_optimizer.tell_runs(run_list)
    config2 = hpl_optimizer.ask_next()
    assert isinstance(config1, HPLConfig), "Config not HPLConfig"
    assert config1.isValid() == True, "Config is not valid"

    assert config1 != config2, "Optimizer did not learn"
