import sys
from pathlib import Path
from typing import List
import pandas as pd
import pytest
sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLResultReader import process_hpl_output, get_hpl_config, get_hpl_runs
from HPLConfig import HPLConfig, HPL_Run, PFactEnum, RFactEnum, BCastEnum, PMapEnum
TEST_SAMPLES_FOLDER = Path(__file__).parent.joinpath("test_samples")

inputs = [
    [
        TEST_SAMPLES_FOLDER.joinpath("hpl_output.log"), 
        HPLConfig(
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
    ],
    [
        TEST_SAMPLES_FOLDER.joinpath("hpl_output_2.log"), 
        HPLConfig(
            N_Array=[99,9,50,84,76],
            NB_Array=[56,9,15,84,76],
            P_Array=[1,1,1,1,1],
            Q_Array=[1,1,1,1,1],
            PFact_Array=[PFactEnum.Left, PFactEnum.Crout, PFactEnum.Right],
            NBMin_Array=[7,1,20,5,5],
            NDIV_Array=[5,2,10,6,12],
            RFact_Array=[RFactEnum.Left, RFactEnum.Right, RFactEnum.Crout],
            BCAST_Array=[BCastEnum.TwoRingM, BCastEnum.TwoRing, BCastEnum.OneRing],
            Depth_Array=[3,3,4,3,0],
        )
    ]
]

@pytest.mark.parametrize("file_path,sample_config", inputs)
def test_process_hpl_output(file_path,sample_config):
    dataframe : pd.DataFrame = process_hpl_output(file_path)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"

@pytest.mark.parametrize("file_path,sample_config", inputs)
def test_get_hpl_config(file_path,sample_config):
    # Test the get_hpl_config function

    config : HPLConfig = get_hpl_config(file_path)

    print(config)
    print(sample_config)
    assert config == sample_config
    
    pass 
@pytest.mark.parametrize("file_path,sample_config", inputs)
def test_get_hpl_runs(file_path,sample_config):
    hplruns = get_hpl_runs(file_path)

    for run in hplruns:
        print(run)

    assert len(hplruns) >0, "Number of runs is 0"

    df = pd.DataFrame([run.__dict__ for run in hplruns])

    assert df['Gflops'].dtype == float, "Gflops column is not float"
    assert df['PFact'].dtype == PFactEnum, "PFact column is not PFactEnum"
    assert df['RFact'].dtype == RFactEnum, "RFact column is not RFactEnum"
    assert df['BCast'].dtype == BCastEnum, "BCast column is not BCastEnum"
    print(df)
    df.to_csv(Path(__file__).parent.joinpath(f"test_results/{file_path.name} hpl_runs.csv"), index=False)
