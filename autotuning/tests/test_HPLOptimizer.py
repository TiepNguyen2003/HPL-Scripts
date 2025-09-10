import sys
from pathlib import Path
from typing import List
import pandas as pd
import pytest
sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLResultReader import process_hpl_output, get_hpl_config, get_hpl_runs
from HPLConfig import HPLConfig, HPL_Run, PFactEnum, RFactEnum, BCastEnum, PMapEnum

sys.path.append(str(Path(__file__).parent.parent.joinpath("src/Optimizer").resolve()))
from HPLOptimizer import HPLOptimizer

HPL_OUTPUT_FILE= Path(__file__).parent.joinpath("test_samples/hpl_output.log")

hpl_optimizer = HPLOptimizer()

def test_tell():
    run_list : List[HPL_Run]  = get_hpl_runs(HPL_OUTPUT_FILE)
    for run in run_list:
        hpl_optimizer.tell_run(run)
    
    

def test_ask():
    test_tell()
    config = hpl_optimizer.ask_next()

    assert isinstance(config, HPLConfig), "Config not HPLConfig"
    assert config.isValid() == True, "Config is not valid"
