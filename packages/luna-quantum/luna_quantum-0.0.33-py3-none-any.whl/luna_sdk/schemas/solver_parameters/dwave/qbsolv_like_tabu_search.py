from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter
from luna_sdk.schemas.solver_parameters.dwave import QBSOLVLike, Tabu


class QbSolvLikeTabuSearchParameters(BaseParameter):
    """
    QBSolv Like Tabu Search breaks down the problem and solves the parts individually using a classic solver that uses Tabu Search.
    This particular implementation uses hybrid.TabuSubproblemSampler (https://docs.ocean.dwavesys.com/projects/hybrid/en/stable/reference/samplers.html#tabusubproblemsampler)
    as a sampler for the subproblems to achieve a QBSolv like behaviour.

    Parameters
    ----------
    qbsolv_like: QBSOLVLike
        Parameters for the QbSolveLike solver.
    tabu_search: Tabu
        Parameters for the Tabu Search.
    """

    qbsolv_like: QBSOLVLike = QBSOLVLike()
    tabu_search: Tabu = Tabu()
