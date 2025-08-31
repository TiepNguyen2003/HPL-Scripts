import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.joinpath("src/HPLWrapper").resolve()))

from HPLConfig import HPLConfig
from HPLRunner import HPLRunner
import pandas as pd

config = HPLConfig(
    N_Array=[26500],
    NB_Array=[100],
    P_Array=[4],
    Q_Array=[2],
    PFact_Array=[0, 1, 2],
    NBMin_Array=[1, 2],
    NDIV_Array=[2],
    RFact_Array=[0, 1, 2],
    BCAST_Array=[0],
    Depth_Array=[0],
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