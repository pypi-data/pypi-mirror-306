from pydantic import BaseModel, ConfigDict

from luna_sdk.schemas.solver_parameters.ibm.standard_parameters import (
    StandardParameters,
)


class QaoaConfig(BaseModel):
    """
    Parameters
    ----------
    reps : int
        Depth of the circuit. Default: 1.
    name : str
        Name of the circuit. Default: "QAOA".
    """

    reps: int = 1
    name: str = "QAOA"

    model_config = ConfigDict(extra="forbid")


class QaoaParameters(StandardParameters):
    """
    The Quantum Approximate Optimization Algorithm ([QAOA](https://arxiv.org/abs/1411.4028))
    solves combinatorial optimization problems by approximating the solution:

    For a given problem represented as a cost Hamiltonian we formulate two unitary
    operators.
    The QAOA solves the problem by iteratively applying the two unitary operators on
    the cost Hamiltonian for a number of steps p.
    The angles for the unitary operators are iteratively updated by measuring the state
    after applying these (like in VQE).

    For further information see qiskit's [QAOA tutorial](https://learning.quantum.ibm.com/tutorial/quantum-approximate-optimization-algorithm).

    Parameters
    ----------
    backend : str | dict[str, Any] | None
        Which backend to use. Default: "AerSimulator"
        - If None, will use no backend and StatevectorSampler and StatevectorEstimator.
        - If dict, will call `runtime_service.least_busy` with the params given in the dict.
        - If str:
            - If "AerSimulator": use AerSimulator
            - If string starts with "Fake, will use the corresponding fake backend from `qiskit_ibm_runtime.fake_provider`.
            - Otherwise, will try to use a real backend with this name.
    shots : int = 1024
        Shots for the optimizer. Default: 1024
    dynamical_decoupling : dict[str, Any] = {}
        Dynamical decoupling options for the optimizer. Default: {}
    optimizer : str
        Name of the optimizer to use in scipy minimize. Default: "COBYLA"
    maxiter : int
        Maximum number of iterations for the algorithm. Default: 10
    optimization_level : int
        Optmimization level for the pass manager. Default: 2
    service_config : ServiceConfig
        Parameters to be passed to the `QiskitRuntimeService` object.
    qaoa_config : QaoaConfig
        Configuration for the QAOAAnsatz; see `qiskit.circuit.library.QAOAAnsatz`.
    """

    qaoa_config: QaoaConfig = QaoaConfig()
