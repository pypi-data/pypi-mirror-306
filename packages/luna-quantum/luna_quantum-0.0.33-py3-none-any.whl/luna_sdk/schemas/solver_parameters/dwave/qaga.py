from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class QAGAParameters(BaseParameter):
    """
    Parameters for the Quantum Assisted Genetic Algorithm (QAGA).
    QAGA combines the principles of genetic algorithms and quantum annealing to solve optimization problems.

    Parameters
    ----------
    p_size: int
        Size of the population.
    p_inc_num: int
        Number of individuals that are added to the population size after each iteration.
    p_max: Optional[int]
        Maximum size of the population.
    pct_random_states: float
        Percentage of random states that are added to the population after each iteration.
    mut_rate: float
        Mutation rate, i.e., probability to mutate an individual. Min: 0.0, Max: 1.0
    rec_rate: int
        Recombination rate, i.e. number of mates each individual is recombined with after each iteration
    rec_method: Literal['cluster_moves', 'one_point_crossover', 'random_crossover']
        The recombination method for the genetic algorithm.
    select_method: Literal['simple', 'shared_energy']
        Method used for the selection phase in the genetic algorithm.
    target: Optional[float]
        Energy level that the algorithm tries to reach. If `None`, the algorithm will run until any other stopping criterion is reached.
    atol: float
        Absolute tolerance used to compare the energies of the target and the individuals.
    rtol: float
        Relative tolerance used to compare the energies of the target and the individuals.
    timeout: float
        The total solving time after which the solver should be stopped. This total solving time includes preprocessing, network overhead when communicating with DWave's API, as well as the actual annealing time.
    max_iter: Optional[int]
        Maximum number of iterations after which the algorithm will stop.
    """

    p_size: int = 20
    p_inc_num: int = 5
    p_max: Optional[int] = 160
    pct_random_states: float = 0.25
    mut_rate: float = Field(default=0.5, ge=0.0, le=1.0)
    rec_rate: int = 1
    rec_method: Literal["cluster_moves", "one_point_crossover", "random_crossover"] = (
        "random_crossover"
    )
    select_method: Literal["simple", "shared_energy"] = "simple"
    target: Optional[float] = None
    atol: float = 0.0
    rtol: float = 0.0
    timeout: float = 60.0
    max_iter: Optional[int] = 100
