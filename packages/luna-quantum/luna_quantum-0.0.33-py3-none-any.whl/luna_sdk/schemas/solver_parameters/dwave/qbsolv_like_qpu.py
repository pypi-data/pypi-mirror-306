from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter
from luna_sdk.schemas.solver_parameters.dwave import QBSOLVLike, Qpu


class QbSolvLikeQpuParameters(BaseParameter):
    """
    QBSolv QPU splits the problem into parts and solves them using the Tabu Search algorithm. For this purpose, the DWaveSampler is used.

    Parameters
    ----------
    qbsolv_like: QBSOLVLike
        Parameters for the QBSOLV-like solver.
    qpu: Qpu
        QPU parameters
    """

    qbsolv_like: QBSOLVLike = QBSOLVLike()
    qpu: Qpu = Qpu()
