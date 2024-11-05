from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class RRQuantumAnnealingSamplingParams(BaseParameter):
    """
    Parameters
    ----------
    anneal_offsets: Optional[Any]
        Anneal offsets for the sampling.
    annealing_time: Optional[Any]
        Annealing time for the sampling.
    auto_scale: Optional[Any]
        Whether to auto scale for the sampling.
    flux_biases: Optional[Any]
        Flux biases for the sampling.
    flux_drift_compensation: bool
        Whether to use flux drift compensation.
    h_gain_schedule: Optional[Any]
        H gain schedule for the sampling.
    max_answers: Optional[int]
        Maximum number of answers for the sampling. Min: 1
    programming_thermalization: Optional[float]
        Programming thermalization for the sampling. Has to be positive.
    readout_thermalization: Optional[float]
        Readout thermalization for the sampling. Has to be positive.
    reduce_intersample_correlation: bool
        Whether to reduce intersample correlation for the sampling.
    """

    anneal_offsets: Optional[Any] = None
    annealing_time: Optional[Any] = None
    auto_scale: Optional[Any] = None
    flux_biases: Optional[Any] = None
    flux_drift_compensation: bool = True
    h_gain_schedule: Optional[Any] = None
    max_answers: Optional[int] = Field(default=None, ge=1)
    programming_thermalization: Optional[float] = Field(default=None, gt=0)
    readout_thermalization: Optional[float] = Field(default=None, gt=0)
    reduce_intersample_correlation: bool = False


class RepeatedReverseQuantumAnnealingParameters(BaseParameter):
    """
    Repeated Reverse Quantum Annealing begins the annealing process from a previously initialized state and increases the temperature from there.
    Afterwards, the temperature is decreased again until the solution is found.
    This procedure is repeated several times with this particular solver. (for additional information see: D-Wave Reverse Annealing)

    Parameters
    ----------
    sampling_params: RRQuantumAnnealingSamplingParams
        Parameters for the RRQuantumAnnealingSamplingParams. See https://docs.dwavesys.com/docs/latest/c_solver_parameters.html for more details.
    initial_states: Optional[List[Dict[str, int]]]
        Initial states for the solver. For each list element `state`, one call to the sampler with the parameter `initial_state=state` will be made in the first iteration.
    n_initial_states: int
        Number of initial states to create when `initial_states` is None. If `initial_states` is not None, this parameter will be ignored. Min: 1
    samples_per_state: int
        How many samples to create per state in each iteration after the first. Min: 1
    beta_schedule: List[float]
        Beta schedule for the solver.
    timeout: float
        Timeout for the solver.
    max_iter: int
        Maximum number of iterations for the solver.
    target: Optional[Any]
        The target energy for the solving process.
    check_trivial: bool
        Whether to check for trivial variables. Checking for trivial variables means an overhead. On the other hand, when set to `False`, trivial variables, i.e., variables without interactions, will lead to a runtime error.
    """

    sampling_params: RRQuantumAnnealingSamplingParams = (
        RRQuantumAnnealingSamplingParams()
    )
    initial_states: Optional[List[Dict[str, int]]] = None
    n_initial_states: int = Field(default=1, ge=1)
    samples_per_state: int = Field(default=1, ge=1)
    beta_schedule: List[float] = [0.5, 3]
    timeout: float = 300
    max_iter: int = 10
    target: Optional[Any] = None
    check_trivial: bool = True
