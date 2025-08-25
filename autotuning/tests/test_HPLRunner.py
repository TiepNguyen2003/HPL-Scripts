import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
from HPLConfig import HPLConfig
from HPLRunner import HPLRunner, HPL_RESULT_FOLDER
import pandas as pd

config = HPLConfig(
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

def test_setconfig():
    runner = HPLRunner()
    runner.setconfig(config)
    assert runner.config == config

def test_runHPL():
    result_path = HPL_RESULT_FOLDER.joinpath("hpl_output.log")

    runner = HPLRunner()
    runner.setconfig(config)
    dataframe: pd.DataFrame = runner.runHPL()

    dataframe.to_csv(Path(__file__).parent.joinpath("test_results/hpl_output.csv"), index=False)
    assert result_path.exists(), f"{result_path} was not created"
    assert isinstance(dataframe, pd.DataFrame), "Dataframe is None"
    assert dataframe['Gflops'].dtype == float, "Gflops column is not float"