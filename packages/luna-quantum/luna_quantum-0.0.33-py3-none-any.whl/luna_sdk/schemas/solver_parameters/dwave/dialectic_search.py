from typing import Optional

from pydantic import Field

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter
from luna_sdk.schemas.solver_parameters.dwave import Decomposer, Loop, Tabu


class DialecticSearchParameters(BaseParameter):
    """
    The Dialectic Search Solver uses a path search between two states representing the thesis and antithesis.
    A greedy search is used to reduce the energy by applying bit flips in an attempt to find the solution.

    decomposer: Decomposer
        Decomposer parameters.
    tabu_antithesis: Tabu
        Tabu parameters for the antithesis phase.
    tabu_synthesis: Tabu
        Tabu parameters for the synthesis phase.
    loop: Loop
        Parameters for the main loop of the algorithm.
    max_tries: Optional[int]
        Maximum number of times the synthesis phase is run for the **same** input state.
        On each improvement, the better state is used for the next input state, and the
        try/trial counter is reset.
    """

    decomposer: Decomposer = Decomposer()
    tabu_antithesis: Tabu = Tabu()
    tabu_synthesis: Tabu = Tabu()
    loop: Loop = Loop()
    max_tries: Optional[int] = Field(default=100, ge=1)
