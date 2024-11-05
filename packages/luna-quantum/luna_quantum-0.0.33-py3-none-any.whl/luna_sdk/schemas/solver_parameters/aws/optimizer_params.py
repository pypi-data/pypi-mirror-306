from typing import Any, Optional, List, Tuple, Dict, Literal
from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class OptimizerParams(BaseParameter):
    """
    Parameters for scipy optimizer

    Attributes
    ----------
    method: Literal
        Type of solver. Currently available methods:
        Nelder-Mead, Powell, CG, BFGS, L-BFGS-B, TNC, COBYLA, COBYQA, SLSQP, trust-constr
    bounds: Optional[list[[tuple[float, float]]]]
        Bounds on variables for Nelder-Mead, L-BFGS-B, TNC, SLSQP, Powell, trust-constr,
        and COBYLA methods. Sequence of (min, max) pairs for each element in x.
        None is used to specify no bound.
    tol: Optional[float]
        Tolerance for termination. When tol is specified, the selected minimization
        algorithm sets some relevant solver-specific tolerance(s) equal to tol.
        For detailed control, use solver-specific options.
    options: Optional[dict[str, Any]]
        A dictionary of solver options.
    """

    method: Literal[
        "Nelder-Mead",
        "Powell",
        "CG",
        "BFGS",
        "L-BFGS-B",
        "TNC",
        "COBYLA",
        "COBYQA",
        "SLSQP",
        "trust-constr",
    ] = "COBYLA"
    bounds: Optional[List[Tuple[float, float]]] = None
    tol: Optional[float] = None
    options: Optional[Dict[str, Any]] = {"maxiter": 20}
