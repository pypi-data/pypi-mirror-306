from typing import List, Optional, Union

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class LeapHybridCqmParameters(BaseParameter):
    """
    Leap's quantum-classical hybrid solvers are intended to solve arbitrary application
    problems formulated as quadratic models.
    This solver accepts arbitrarily structured problems formulated as CQMs, with any
    constraints represented natively.

    Parameters
    ----------
    time_limit: Union[float, int, NoneType]
        The time limit for the solver.
    spin_variables: Optional[List[str]]
        The list of spin variables.
    """

    time_limit: Optional[Union[float, int]] = None
    spin_variables: Optional[List[str]] = None
