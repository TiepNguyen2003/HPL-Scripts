import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.joinpath("src/HPLWrapper").resolve()))
sys.path.append(str(Path(__file__).parent.joinpath("src/Optimizer").resolve()))

from incrementalOptimizer import IncrementalOptimizer
from HPLConfig import HPLConfig
from HPLResultReader import is_hpl_config

RUN_FOLDER= Path(__file__).parent.joinpath("results","logs")



if __name__ == "__main__":

    optimizer : IncrementalOptimizer = IncrementalOptimizer()

    for path in RUN_FOLDER.iterdir():
        if path.is_file() and is_hpl_config(path) is True:
            optimizer.process_file(path)
    optimizer.set_next_config()

    optimizer.hplrunner.runHPL()

    for path in RUN_FOLDER.iterdir():
        if path.is_file() and is_hpl_config(path) is True:
            optimizer.process_file(path)






