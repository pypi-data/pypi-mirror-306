from typing import Optional

from pydantic import Field

from luna_sdk.schemas.solver_parameters.fujitsu.base import (
    CommonParams,
    ConnectionParams,
)


class DigitalAnnealerV3Parameters(CommonParams, ConnectionParams):
    """
    From the [Fujitsu website](https://www.fujitsu.com/global/services/business-services/digital-annealer/):
    Fujitsu's Digital Annealer provides an alternative to quantum computing
    technology, which is at present both very expensive and difficult to run. Using a
    digital circuit design inspired by quantum phenomena, the Digital Annealer focuses
    on rapidly solving complex combinatorial optimization problems without the added
    complications and costs typically associated with quantum computing methods.

    Parameters
    ----------
    annealer_protocol: Literal['http', 'https']
        Protocol for Digital Annealer REST access: 'http' or 'https'.
    annealer_address: str
        IP address of the host machine of Digital Annealer.
    annealer_port: int
        Port of Digital Annealer service on the host machine. Min: 0, Max: 2**16
    annealer_path: str
        Path prefix used as common root for all REST productions.
    request_mode: Literal['stream', 'simple', 'gzip']
        Defines how the request should be sent.
    annealer_queue_size: int
        Size of Digital Annealer queue for selected service.
    timeout: int
        Timeout for a single http(s)-request in seconds.
    auto_tuning: Literal['NOTHING', 'SCALING', 'AUTO_SCALING', 'SAMPLING', 'AUTO_SCALING_AND_SAMPLING', 'SCALING_AND_SAMPLING']
        Following methods for scaling `qubo` and determining temperatures are available:
        AutoTuning.NOTHING: no action
        AutoTuning.SCALING: `scaling_factor` is multiplied to `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
        AutoTuning.AUTO_SCALING: A maximum scaling factor w.r.t. `scaling_bit_precision` is multiplied to `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
        AutoTuning.SAMPLING: `temperature_start`, `temperature_end` and `offset_increase_rate` are automatically determined.
        AutoTuning.AUTO_SCALING_AND_SAMPLING: Temperatures and scaling factor are automatically determined and applied.
    scaling_factor: Union[int, float]
        The scaling factor for `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
    scaling_bit_precision: int
        Maximum `scaling_bit_precision` for `qubo`. Used to define the scaling factor for `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
    guidance_config: Optional[PartialConfig]
        Specifies an initial value for each polynomial (problem) variable that is set to find an optimal solution. By specifying a value that is close to the optimal solution, improvement in the accuracy of the optimal solution can be expected. If you repeatedly use the specified initial values to solve the same polynomial (problem), the same optimal solution is obtained each time.
    random_seed: Optional[int]
        Seed for random numbers for the optimization call. Min: 0, Max: 9_999
    timeseries_max_bits: Optional[int]
        Maximum number of bits for timeseries.
    solver_max_bits: int
        Maximum number of bits on selected solver.
    time_limit_sec: Optional[int]
        Maximum running time of DA in seconds. Specifies the upper limit of running time of DA. Min: 1, Max: 1_800
    target_energy: Optional[int]
        Threshold energy for fast exit. This may not work correctly if the specified value is larger than its max value or lower than its min value. Min: -99_999_999_999, Max: 99_999_999_999
    num_group: int
        Number of independent optimization processes. Increasing the number of independent optimization processes leads to better coverage of the search space. Note: Increasing this number requires to also increase `time_limit_sec` such that the search time for each process is sufficient. Min: 1, Max: 16
    num_solution: int
        Number of solutions maintained and updated by each optimization process. Min: 1, Max: 16
    num_output_solution: int
        Maximal number of the best solutions returned by each optimization. Total number of results is `num_solution` * `num_group`. Min: 1, Max: 1_024
    gs_num_iteration_factor: int
        Maximal number of iterations in one epoch of the global search in each optimization is `gs_num_iteration_factor` * number of bits. Min: 0, Max: 100
    gs_num_iteration_cl: int
        Maximal number of iterations without improvement in one epoch of the global search in each optimization before terminating and continuing with the next epoch. For problems with very deep local minima having a very low value is helpful. Min: 0, Max: 1_000_000
    gs_penalty_auto_mode: int
        Parameter to choose whether to automatically incrementally adapt `gs_penalty_coef` to the optimal value.
        0: Use `gs_penalty_coef` as the fixed factor to weight the penalty polynomial during optimization.
        1: Start with `gs_penalty_coef` as weight factor for penalty polynomial and automatically and incrementally increase this factor during optimization by multiplying `gs_penalty_inc_rate` / 100 repeatedly until `gs_max_penalty_coef` is reached or the penalty energy is zero.
    gs_penalty_coef: int
        Factor to weight the penalty polynomial. If `gs_penalty_auto_mode` is 0, this value does not change. If `gs_penalty_auto_mode` is 1, this initial weight factor is repeatedly increased by `gs_penalty_inc_rate` until `gs_max_penalty_coef` is reached or the penalty energy is zero. Min: 1, Max: 2**63 - 1
    gs_penalty_inc_rate: int
        Only used if `gs_penalty_auto_mode` is 1. In this case, the initial weight factor `gs_penalty_coef` for the penalty polynomial is repeatedly increased by multiplying `gs_penalty_inc_rate` / 100 until `gs_max_penalty_coef` is reached or the penalty energy is zero. Min: 100, Max: 200
    gs_max_penalty_coef: int
        Maximal value for the penalty coefficient. If `gs_penalty_auto_mode` is 0, this is the maximal value for `gs_penalty_coef`. If `gs_penalty_auto_mode` is 1, this is the maximal value to which `gs_penalty_coef` can be increased during the automatic adjustment. If `gs_max_penalty_coef` is set to 0, then the maximal penalty coefficient is 2^63 - 1. Min: 0, Max: 2**63 - 1
    annealer_protocol: Literal['http', 'https']
        Protocol for Digital Annealer REST access: 'http' or 'https'.
    annealer_address: str
        IP address of the host machine of Digital Annealer.
    annealer_port: int
        Port of Digital Annealer service on the host machine. Min: 0, Max: 2**16
    annealer_path: str
        Path prefix used as common root for all REST productions.
    request_mode: Literal['stream', 'simple', 'gzip']
        Defines how the request should be sent.
    annealer_queue_size: int
        Size of Digital Annealer queue for selected service.
    timeout: int
        Timeout for a single http(s)-request in seconds.
    auto_tuning: Literal['NOTHING', 'SCALING', 'AUTO_SCALING', 'SAMPLING', 'AUTO_SCALING_AND_SAMPLING', 'SCALING_AND_SAMPLING']
        Following methods for scaling `qubo` and determining temperatures are available:
        AutoTuning.NOTHING: no action
        AutoTuning.SCALING: `scaling_factor` is multiplied to `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
        AutoTuning.AUTO_SCALING: A maximum scaling factor w.r.t. `scaling_bit_precision` is multiplied to `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
        AutoTuning.SAMPLING: `temperature_start`, `temperature_end` and `offset_increase_rate` are automatically determined.
        AutoTuning.AUTO_SCALING_AND_SAMPLING: Temperatures and scaling factor are automatically determined and applied.
    scaling_factor: Union[int, float]
        The scaling factor for `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
    scaling_bit_precision: int
        Maximum `scaling_bit_precision` for `qubo`. Used to define the scaling factor for `qubo`, `temperature_start`, `temperature_end` and `offset_increase_rate`.
    guidance_config: Optional[PartialConfig]
        Specifies an initial value for each polynomial (problem) variable that is set to find an optimal solution. By specifying a value that is close to the optimal solution, improvement in the accuracy of the optimal solution can be expected. If you repeatedly use the specified initial values to solve the same polynomial (problem), the same optimal solution is obtained each time.
    random_seed: Optional[int]
        Seed for random numbers for the optimization call. Min: 0, Max: 9_999
    timeseries_max_bits: Optional[int]
        Maximum number of bits for timeseries.
    solver_max_bits: int
        Maximum number of bits on selected solver.
    time_limit_sec: Optional[int]
        Maximum running time of DA in seconds. Specifies the upper limit of running time of DA. Min: 1, Max: 1_800
    target_energy: Optional[int]
        Threshold energy for fast exit. This may not work correctly if the specified value is larger than its max value or lower than its min value. Min: -99_999_999_999, Max: 99_999_999_999
    num_group: int
        Number of independent optimization processes. Increasing the number of independent optimization processes leads to better coverage of the search space. Note: Increasing this number requires to also increase `time_limit_sec` such that the search time for each process is sufficient. Min: 1, Max: 16
    num_solution: int
        Number of solutions maintained and updated by each optimization process. Min: 1, Max: 16
    num_output_solution: int
        Maximal number of the best solutions returned by each optimization. Total number of results is `num_solution` * `num_group`. Min: 1, Max: 1_024
    gs_num_iteration_factor: int
        Maximal number of iterations in one epoch of the global search in each optimization is `gs_num_iteration_factor` * number of bits. Min: 0, Max: 100
    gs_num_iteration_cl: int
        Maximal number of iterations without improvement in one epoch of the global search in each optimization before terminating and continuing with the next epoch. For problems with very deep local minima having a very low value is helpful. Min: 0, Max: 1_000_000
    gs_penalty_auto_mode: int
        Parameter to choose whether to automatically incrementally adapt `gs_penalty_coef` to the optimal value.
        0: Use `gs_penalty_coef` as the fixed factor to weight the penalty polynomial during optimization.
        1: Start with `gs_penalty_coef` as weight factor for penalty polynomial and automatically and incrementally increase this factor during optimization by multiplying `gs_penalty_inc_rate` / 100 repeatedly until `gs_max_penalty_coef` is reached or the penalty energy is zero.
    gs_penalty_coef: int
        Factor to weight the penalty polynomial. If `gs_penalty_auto_mode` is 0, this value does not change. If `gs_penalty_auto_mode` is 1, this initial weight factor is repeatedly increased by `gs_penalty_inc_rate` until `gs_max_penalty_coef` is reached or the penalty energy is zero. Min: 1, Max: 2**63 - 1
    gs_penalty_inc_rate: int
        Only used if `gs_penalty_auto_mode` is 1. In this case, the initial weight factor `gs_penalty_coef` for the penalty polynomial is repeatedly increased by multiplying `gs_penalty_inc_rate` / 100 until `gs_max_penalty_coef` is reached or the penalty energy is zero. Min: 100, Max: 200
    gs_max_penalty_coef: int
        Maximal value for the penalty coefficient. If `gs_penalty_auto_mode` is 0, this is the maximal value for `gs_penalty_coef`. If `gs_penalty_auto_mode` is 1, this is the maximal value to which `gs_penalty_coef` can be increased during the automatic adjustment. If `gs_max_penalty_coef` is set to 0, then the maximal penalty coefficient is 2^63 - 1. Min: 0, Max: 2**63 - 1
    """

    time_limit_sec: Optional[int] = Field(default=None, ge=1, le=1_800)
    target_energy: Optional[int] = Field(
        default=None, ge=-99_999_999_999, le=99_999_999_999
    )
    num_group: int = Field(default=1, ge=1, le=16)
    num_solution: int = Field(default=16, ge=1, le=16)
    num_output_solution: int = Field(default=5, ge=1, le=1_024)
    gs_num_iteration_factor: int = Field(default=5, ge=0, le=100)
    gs_num_iteration_cl: int = Field(default=800, ge=0, le=1_000_000)
    gs_penalty_auto_mode: int = Field(default=1, ge=0, le=1)
    gs_penalty_coef: int = Field(default=1, ge=1, le=2**63 - 1)
    gs_penalty_inc_rate: int = Field(default=150, ge=100, le=200)
    gs_max_penalty_coef: int = Field(default=0, ge=0, le=2**63 - 1)
