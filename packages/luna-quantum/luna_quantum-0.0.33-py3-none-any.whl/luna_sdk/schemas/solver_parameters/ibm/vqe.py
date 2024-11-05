from typing import Any, Dict

from luna_sdk.schemas.solver_parameters.ibm.standard_parameters import (
    StandardParameters,
)


class VqeParameters(StandardParameters):
    """
    The Variational Quantum Eigensolver ([VQE](https://arxiv.org/abs/1304.3061)) solves
    combinatorial optimization problems by approximating the solution:
    \n For a given problem represented as a cost Hamiltonian we apply
    a classical/quantum hybrid algorithm to find the solution. The VQE solves
    the problem by iteratively applying a linear transformation
    (variational form) on the cost Hamiltonian and optimizing the parameters of
    the transformation using a classical optimizer.

    For further information see qiskit's [VQE tutorial](https://learning.quantum.ibm.com/tutorial/variational-quantum-eigensolver).

    Parameters
    ----------
    backend : str | dict[str, Any] | None
        Which backend to use. Default: "AerSimulator"
        - If None, will use no backend and StatevectorSampler and StatevectorEstimator.
        - If dict, will call `runtime_service.least_busy` with the params given in the dict.
        - If str:
            - If "AerSimulator": use AerSimulator
            - If string starts with "Fake, will use the corresponding fake backend from qiskit_ibm_runtime.fake_provider
            - Otherwise, will try to use a real backend with this name
    shots : int
        Shots for the optimizer. Default: 1024
    dynamical_decoupling : dict[str, Any]
        Dynamical decoupling options for the optimizer. Default: {}
    optimizer : str
        Name of the optimizer to use in scipy minimize. Default: "COBYLA"
    maxiter : int
        Maximum number of iterations for the algorithm. Default: 10
    optimization_level : int
        Optmimization level for the pass manager. Default: 2
    service_config : ServiceConfig
        Parameters to be passed to the `QiskitRuntimeService` object.
    ansatz : str
        Which ansatz to use from `qiskit.circuit.library`. Default: "EfficientSU2"
    ansatz_config : dict[str, Any]
        Configuration for the ansatz. Default: {}
    """

    ansatz: str = "EfficientSU2"
    ansatz_config: Dict[str, Any] = {}
