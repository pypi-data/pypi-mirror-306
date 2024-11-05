from pydantic import Field

from luna_sdk.schemas.solver_parameters.fujitsu.base import (
    CommonParams,
    ConnectionParams,
    V2Params,
)


class DigitalAnnealerV2Parameters(CommonParams, V2Params, ConnectionParams):
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
    optimization_method: Literal['annealing', 'parallel_tempering']
        Digital Annealer optimization algorithm.
    temperature_start: float
        Start temperature of the annealing process. Min: 0.0, Max: 1e20
    temperature_end: float
        End temperature of the annealing process. Min: 0.0, Max: 1e20
    temperature_mode: int
        Cooling curve mode for temperature decay.
        0, 'EXPONENTIAL': Reduce temperature by factor `1 - temperature_decay` every temperature_interval steps
        1, 'INVERSE': Reduce temperature by factor `1 - temperature_decay * temperature` every temperature_interval steps
        2, 'INVERSE_ROOT': Reduce temperature by factor `1 - temperature_decay * temperature` every temperature_interval steps.
    temperature_interval: int
        Number of iterations keeping temperature constant. Min: 1, Max: 1e20
    offset_increase_rate: float
        Increase of dynamic offset when no bit is selected. Set to 0.0 to switch off dynamic energy feature. Min: 0.0, Max: 1e20
    solution_mode: Literal['QUICK', 'COMPLETE']
        Defines how many solutions should be created. 'COMPLETE' returns all runs best configuration, 'QUICK' returns overall best configuration only.
    flip_probabilities: Tuple[float, float]
        Parameter for determining the start temperature. This parameter indicates the acceptance probability of an energy increase (worsening) in the annealing process at the calculated start temperature.
    annealing_steps: Tuple[float, float]
        `annealing_steps` stands for the portion of annealing steps, where `end_progress_probability` is reached.
    sampling_runs: int
        Sub-parameter used to define the energy deltas during the internal energy sampling procedure for annealing parameter estimation. `sampling_runs` is the number of random walkers started for energy deltas determination.
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
    number_runs: int
        Number of stochastically independent runs. Min: 16, Max: 128
    number_replicas: int
        Number of replicas in parallel tempering. Min: 26, Max: 128
    number_iterations: int
        Total number of iterations per run. Min: 1, Max: 2_000_000_000
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
    optimization_method: Literal['annealing', 'parallel_tempering']
        Digital Annealer optimization algorithm.
    temperature_start: float
        Start temperature of the annealing process. Min: 0.0, Max: 1e20
    temperature_end: float
        End temperature of the annealing process. Min: 0.0, Max: 1e20
    temperature_mode: int
        Cooling curve mode for temperature decay.
        0, 'EXPONENTIAL': Reduce temperature by factor `1 - temperature_decay` every temperature_interval steps
        1, 'INVERSE': Reduce temperature by factor `1 - temperature_decay * temperature` every temperature_interval steps
        2, 'INVERSE_ROOT': Reduce temperature by factor `1 - temperature_decay * temperature` every temperature_interval steps.
    temperature_interval: int
        Number of iterations keeping temperature constant. Min: 1, Max: 1e20
    offset_increase_rate: float
        Increase of dynamic offset when no bit is selected. Set to 0.0 to switch off dynamic energy feature. Min: 0.0, Max: 1e20
    solution_mode: Literal['QUICK', 'COMPLETE']
        Defines how many solutions should be created. 'COMPLETE' returns all runs best configuration, 'QUICK' returns overall best configuration only.
    flip_probabilities: Tuple[float, float]
        Parameter for determining the start temperature. This parameter indicates the acceptance probability of an energy increase (worsening) in the annealing process at the calculated start temperature.
    annealing_steps: Tuple[float, float]
        `annealing_steps` stands for the portion of annealing steps, where `end_progress_probability` is reached.
    sampling_runs: int
        Sub-parameter used to define the energy deltas during the internal energy sampling procedure for annealing parameter estimation. `sampling_runs` is the number of random walkers started for energy deltas determination.
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
    number_runs: int
        Number of stochastically independent runs. Min: 16, Max: 128
    number_replicas: int
        Number of replicas in parallel tempering. Min: 26, Max: 128
    number_iterations: int
        Total number of iterations per run. Min: 1, Max: 2_000_000_000
    """

    number_runs: int = Field(default=16, ge=16, le=128)
    number_replicas: int = Field(default=26, ge=26, le=128)
    number_iterations: int = Field(default=1_000_000, ge=1, le=2_000_000_000)
