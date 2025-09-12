import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("src/HPLWrapper").resolve()))
sys.path.append(str(Path(__file__).parent.joinpath("src/Optimizer").resolve()))

from incrementalOptimizer import IncrementalOptimizer
from HPLConfig import HPLConfig
from HPLResultReader import is_hpl_config
from config import RESULTS_PATH
RUN_FOLDER= RESULTS_PATH.joinpath("logs")



if __name__ == "__main__":
    print("Creating optimizer")
    optimizer : IncrementalOptimizer = IncrementalOptimizer()
    print("Reading through paths")
    for path in RUN_FOLDER.iterdir():
        if path.is_file() and is_hpl_config(path) is True:
            optimizer.process_file(path)
    print("Predicting config")
    optimizer.set_next_config()
    print("Running config")
    optimizer.hplrunner.runHPL()
    print("Reading through optimized")
    for path in RUN_FOLDER.iterdir():
        if path.is_file() and is_hpl_config(path) is True:
            optimizer.process_file(path)






