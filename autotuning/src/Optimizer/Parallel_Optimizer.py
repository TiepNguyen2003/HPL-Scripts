import numpy as np

from skopt import Optimizer
from skopt.space import Real, Integer, Categorical, Space





hpl_config_space = Space([
    Integer(0,0.8*FullN, name="N"),
    Integer(16,300, name="NB"), # recommended to be 256
    Integer(1,name="P")
])

class ParallelHPLOptimizer:
    def __init__(self):
        self.optimizer = Optimizer(
            dimensions=space.dimensions,
            base_estimator="GP",
            acq_func="LCB",
            acq_optimizer="auto",
            n_initial_points=5,
            random_state=42
        )
