from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter
from luna_sdk.schemas.solver_parameters.dwave import FixedTemperatureSampler, Loop


class ParallelTemperingParameters(BaseParameter):
    """
    Parallel Tempering uses multiple optimization procedures per temperature.
    During the cooling process, an exchange of replicas can take place between the parallel procedures,
    thus enabling higher energy mountains to be overcome.

    Parameters
    ----------
    n_replicas: int
        Number of replicas for the parallel tempering. Default is 2.
    random_swaps_factor: int
        Factor for random swaps. Default is 1.
    fixed_temperature_sampler: FixedTemperatureSampler
        Parameters for the fixed temperature sampler.
    cpu_count_multiplier: int
        Multiplier for the CPU count. Default is 5.
    loop: Loop
        Parameters for the main loop of the algorithm.
    """

    n_replicas: int = 2
    random_swaps_factor: int = 1
    fixed_temperature_sampler: FixedTemperatureSampler = FixedTemperatureSampler()
    cpu_count_multiplier: int = 5
    loop: Loop = Loop()
