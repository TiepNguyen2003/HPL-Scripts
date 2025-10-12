from skopt.space import Space
from skopt.space.space import Categorical, Integer, Real

def is_within_space(space: Space, x) -> bool:
    """
    Check whether a configuration x is within the defined skopt Space.

    Parameters
    ----------
    space : skopt.space.Space
        The search space.
    x : list or array-like
        The configuration to test. Must have the same length as the space.

    Returns
    -------
    bool
        True if x is within the space; False otherwise.
    """
    if len(x) != len(space.dimensions):
        return False

    for val, dim in zip(x, space.dimensions):
        if isinstance(dim, Integer):
            if not isinstance(val, int):
                return False
            if not (dim.low <= val <= dim.high):
                return False
            
            

        elif isinstance(dim, Real):
            if not (dim.low <= val <= dim.high):
                return False
            if not isinstance(val, (float, int)):
                return False

        elif isinstance(dim, Categorical):
            if val not in dim.categories:
                return False

        else:
            raise TypeError(f"Unsupported dimension type: {type(dim)}")

    return True
