import sys
from pathlib import Path
from typing import List
import pandas as pd
import pytest
sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLResultReader import process_hpl_output, get_hpl_config, get_hpl_runs
from HPLConfig import HPLConfig, HPL_Run, PFactEnum, RFactEnum, BCastEnum, PMapEnum
HPL_OUTPUT_FILE= Path(__file__).parent.joinpath("test_samples/hpl_output.log")

output_config = config = HPLConfig(
        N_Array=[30],
        NB_Array=[1],
        P_Array=[1],
        Q_Array=[1],
        PFact_Array=[0, 1, 2],
        NBMin_Array=[1, 2],
        NDIV_Array=[2],
        RFact_Array=[0, 1, 2],
        BCAST_Array=[0],
        Depth_Array=[0],
    )

def test_process_hpl_output():
    dataframe : pd.DataFrame = process_hpl_output(HPL_OUTPUT_FILE)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"

def test_get_hpl_config():
    # Test the get_hpl_config function

    config : HPLConfig = get_hpl_config(HPL_OUTPUT_FILE)

    print(config)
    print(output_config)
    assert config == output_config
    
    pass 

def test_get_hpl_runs():
    hplruns = get_hpl_runs(HPL_OUTPUT_FILE)

    for run in hplruns:
        print(run)

    assert len(hplruns) == 18, "Number of runs is not correct"

    df = pd.DataFrame([run.__dict__ for run in hplruns])

    assert df['Gflops'].dtype == float, "Gflops column is not float"
    assert df['PFact'].dtype == PFactEnum, "PFact column is not PFactEnum"
    assert df['RFact'].dtype == RFactEnum, "RFact column is not RFactEnum"
    assert df['BCast'].dtype == BCastEnum, "BCast column is not BCastEnum"
    print(df)
    df.to_csv(Path(__file__).parent.joinpath("test_results/hpl_runs.csv"), index=False)
