import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLConfig import HPLConfig, BCastEnum, RFactEnum, PFactEnum, PMapEnum
from HPLRunner import HPLRunner
from SLURMConfig import SLURMConfig
import pandas as pd
import shutil
import pytest
from config import NUM_PROCESS 


config1 = HPLConfig(
    N_Array=[100],
    NB_Array=[1],
    P_Array=[NUM_PROCESS],
    Q_Array=[1],
    PFact_Array=[0, 1, 2],
    NBMin_Array=[1, 2],
    NDIV_Array=[2],
    RFact_Array=[0, 1, 2],
    BCAST_Array=[0],
    Depth_Array=[0],
)

config2 = HPLConfig(
    N_Array=[100],
    NB_Array=[1],
    P_Array=[NUM_PROCESS],
    Q_Array=[1],
    PMAP_Process_Mapping= PMapEnum.Column,
    PFact_Array=[PFactEnum.Left, PFactEnum.Crout, PFactEnum.Right],
    NBMin_Array=[1, 2],
    NDIV_Array=[2],
    RFact_Array=[RFactEnum.Left, RFactEnum.Crout, RFactEnum.Right],
    BCAST_Array=[BCastEnum.OneRing, BCastEnum.OneRingM],
    Depth_Array=[0],
)
fatconfig = HPLConfig(
    N_Array=[13000000],
    NB_Array=[1],
    P_Array=[1],
    Q_Array=[1],
    PMAP_Process_Mapping= PMapEnum.Column,
    PFact_Array=[PFactEnum.Left, PFactEnum.Crout, PFactEnum.Right],
    NBMin_Array=[1, 2],
    NDIV_Array=[2],
    RFact_Array=[RFactEnum.Left, RFactEnum.Crout, RFactEnum.Right],
    BCAST_Array=[BCastEnum.OneRing, BCastEnum.OneRingM],
    Depth_Array=[0],
)


def test_setconfig():
    runner = HPLRunner()
    runner.setconfig(config1)
    assert runner.config == config1

def test_runHPL():
    runner = HPLRunner()
    runner.setconfig(config1)
    dataframe: pd.DataFrame = runner.runHPL()

    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output.csv"), index=False)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"

def test_runHPL_2():
    runner = HPLRunner()
    runner.setconfig(config2)
    dataframe: pd.DataFrame = runner.runHPL()

    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output.csv"), index=False)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"


def test_runSLURM():

    if shutil.which("sbatch") is None:
        pytest.skip("No slurm, skip slurm test")

    runner = HPLRunner()
    runner.setconfig(config2)
    dataframe: pd.DataFrame = runner.runHPL()

    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output.csv"), index=False)
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"
# Assert we fail gracefully
def test_runHPL_fat(monkeypatch):
    
    pytest.skip()
    runner = HPLRunner()
    runner._MAXIMUM_HPL_N = 15000000
    runner.setconfig(fatconfig)
    dataframe: pd.DataFrame = runner.runHPL()

    assert dataframe is None, "Dataframe should be None for fat config"