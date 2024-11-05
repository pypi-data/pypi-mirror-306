from typing import Literal, Optional, Tuple

from pydantic import Field

from luna_sdk.schemas.solver_parameters.dwave.qaga import QAGAParameters


class SAGAParameters(QAGAParameters):
    """
    Parameters for the Simulated Annealing Assisted Genetic Algorithm (SAGA).
    SAGA combines the principles of genetic algorithms and simulated annealing to solve optimization problems.

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
    num_sweeps: int
        The number of sweeps for simulated annealing.
    num_sweeps_inc_factor: float
        factor of increasement for `num_sweeps` after each iteration
    num_sweeps_inc_max: Optional[int]
        Maximum number of num_sweeps that may be reached when increasing the `num_sweeps` value.
    beta_range_type: Literal['default', 'percent', 'fixed', 'inc']
        Method that is used to compute the beta range.
                default': the same as percent with values [50, 1]
                'percent': the percentage chance of flipping qubits from hot to cold temperature
                'fixed': a fixed temperature as a value
                'inc': the default or percentage beta range but with decreasing percentages from iteration to iteration
    beta_range: Optional[Tuple[float, float]]
        Explicit beta range that is used for beta_range_type 'fixed' and 'percent'.
    """

    num_sweeps: int = 10
    num_sweeps_inc_factor: float = 1.2
    num_sweeps_inc_max: Optional[int] = 7_000
    beta_range_type: Literal["default", "percent", "fixed", "inc"] = "default"
    beta_range: Optional[Tuple[float, float]] = None
