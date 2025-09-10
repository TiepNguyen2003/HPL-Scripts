import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLConfig import HPLConfig
from HPLRunner import HPLRunner
from SLURMConfig import SLURMConfig
import pandas as pd
import shutil
import pytest


config = HPLConfig(
    N_Array=[1500],
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

slurmConfig = SLURMConfig(
    Nodes=1,
    Partition="test",
    Alloc_GB=32,
    Time="00:20:00",
    Ntasks_perNode=1,
    Job_Name="HPL_Test",
    Mail_User="tiep123@trieuvan.com",
    Mail_Type="ALL"
)

def test_setconfig():
    runner = HPLRunner()
    runner.setconfig(config)
    assert runner.config == config

def test_runHPL():
    runner = HPLRunner()
    runner.setconfig(config)
    dataframe: pd.DataFrame = runner.runHPL()

    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output.csv"), index=False)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"

def test_runHPL_2():
    runner = HPLRunner()
    runner.setconfig(config)
    dataframe: pd.DataFrame = runner.runHPL()

    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output.csv"), index=False)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"


def test_runSLURM():
    pytest.skip()
    if shutil.which("sbatch") is None:
        pytest.skip("No slurm, skip slurm test")

    runner = HPLRunner()
    runner.setconfig(config)
    runner.setSlurmConfig(slurmConfig)
    dataframe: pd.DataFrame = runner.runSLURM()
    
    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output_slurm.csv"), index=False)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"
