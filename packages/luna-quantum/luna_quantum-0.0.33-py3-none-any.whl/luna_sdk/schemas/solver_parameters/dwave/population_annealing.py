from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter
from luna_sdk.schemas.solver_parameters.dwave import FixedTemperatureSampler


class PopulationAnnealingParameters(BaseParameter):
    """
    Population Annealing uses a sequential Monte Carlo method to minimize the energy of a population.
    The population consists of walkers that can explore their neighborhood during the cooling process.
    Afterwards, walkers are removed and duplicated using bias to lower energy.
    Eventually, a population collapse occurs where all walkers are in the lowest energy state.

    Parameters
    ----------
    fixed_temperature_sampler: FixedTemperatureSampler
        Parameters for the fixed temperature sampler.
    max_iter: int
        Maximum number of iterations. Default is 20.
    max_time: int
        Maximum time in seconds that the algorithm is allowed to run. Default is 2.
    """

    fixed_temperature_sampler: FixedTemperatureSampler = FixedTemperatureSampler()
    max_iter: int = 20
    max_time: int = 2
