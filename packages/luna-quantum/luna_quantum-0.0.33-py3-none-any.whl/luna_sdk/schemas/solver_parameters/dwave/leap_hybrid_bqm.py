from typing import Optional, Union

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class LeapHybridBqmParameters(BaseParameter):
    """
    Leap's quantum-classical hybrid solvers are intended to solve arbitrary application
    problems formulated as quadratic models.
    This solver accepts arbitrarily structured, unconstrained problems formulated as
    BQMs, with any constraints typically represented through penalty models.

    Parameters
    ----------
    time_limit: Union[float, int, NoneType]
        The time limit for the solver.
    """

    time_limit: Optional[Union[float, int]] = None
