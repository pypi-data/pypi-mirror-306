from typing import Any, Dict, Literal, Optional, Union

from pydantic import Field

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class Simulator(BaseParameter):
    """Use a simulator as backend. The QAOA is executed completely on our server, and
    no IBM token is required.

    Parameters
    ----------
    backend_name: Literal['aer', 'statevector']
        Which simulator to use. Currently, `AerSimulator` from `qiskit_aer` and the statevector simulator from `qiskit.primitives` are available.
    """

    backend_type: Literal["simulator"] = "simulator"
    backend_name: Literal["aer", "statevector"] = "aer"


class FakeProvider(BaseParameter):
    """Use a V2 fake backend from `qiskit_ibm_runtime.fake_provider`. The QAOA is
    executed entirely on our server, and no IBM token is required.

    Parameters
    ----------
    backend_name: str
        Which backend to use
    """

    backend_type: Literal["fake_provider"] = "fake_provider"
    backend_name: str


class IbmBackend(BaseParameter):
    """Use an online backend from `ibm_quantum` or `ibm_cloud`. As IBM hardware is used,
    this method requires an IBM token.

    Parameters
    ----------
    backend_name: str
        Which backend to use.
    """

    backend_type: Literal["ibm_backend"] = "ibm_backend"
    backend_name: str


class LeastBusyQuery(BaseParameter):
    """Filter parameters when querying the least busy backend.

    Parameters
    ----------
    min_num_qubits: Optional[int]
        Minimum number of qubits the backend has to have.
    instance: Optional[str]
        This is only supported for `ibm_quantum` runtime and is in the hub/group/project format.
    filters: Dict[str, Any]
        Simple filters that require a specific value for an attribute in backend configuration or status. Example: `{'operational': True}`"""

    min_num_qubits: Optional[int] = None
    instance: Optional[str] = None
    filters: Dict[str, Any] = {}


class LeastBusy(BaseParameter):
    """Use the least busy online backend from `ibm_quantum` or `ibm_cloud`. As IBM
    hardware is used, this method requires an IBM token.

    Parameters
    ----------
    query_params: LeastBusyQuery
        Filter parameters when querying the least busy backend.
    """

    backend_type: Literal["least_busy"] = "least_busy"
    query_params: LeastBusyQuery = LeastBusyQuery()


class ServiceConfig(BaseParameter):
    """Parameters to be passed to the `QiskitRuntimeService` object

    Parameters
    ----------
    channel: Optional[Literal['ibm_cloud', 'ibm_quantum']]
        The channel type for the service
    url: Optional[str]
        The URL of the service
    name: Optional[str]
        The name of the service
    instance: Optional[str]
        The instance identifier
    proxies: Optional[dict]
        Proxy settings for the service
    verify: Optional[bool]
        SSL verification setting
    channel_strategy: Optional[str]
        The strategy for the channel
    """

    channel: Optional[Literal["ibm_cloud", "ibm_quantum"]] = "ibm_quantum"
    url: Optional[str] = None
    name: Optional[str] = None
    instance: Optional[str] = None
    proxies: Optional[dict] = None
    verify: Optional[bool] = None
    channel_strategy: Optional[str] = None


class StandardParameters(BaseParameter):
    """
    Standard parameters for the optimizer.

    Parameters
    ----------
    backend: Union[Simulator, FakeProvider, IbmBackend, LeastBusy]
        Which backend to use. If None, will use no backend and StatevectorSampler and StatevectorEstimator. If dict, will call `runtime_service.least_busy` with the params given in the dict. If str: If 'AerSimulator', use AerSimulator. If string starts with 'Fake', will use the corresponding fake backend from qiskit_ibm_runtime.fake_provider. Otherwise, will try to use a real backend with this name.
    shots: int
        Shots for the optimizer
    dynamical_decoupling: Dict[str, Any]
        Dynamical decoupling options for the optimizer
    optimizer: str
        Name of the optimizer to use in scipy minimize
    maxiter: int
        Maximum number of iterations for the algorithm
    optimization_level: int
        Optimization level for the pass manager
    service_config: ServiceConfig
        Parameters to be passed to the `QiskitRuntimeService` object
    """

    backend: Union[Simulator, FakeProvider, IbmBackend, LeastBusy] = Field(
        default=Simulator(), discriminator="backend_type"
    )
    shots: int = 1024
    dynamical_decoupling: Dict[str, Any] = {}
    optimizer: str = "COBYLA"
    maxiter: int = 10
    optimization_level: int = 2
    service_config: ServiceConfig = ServiceConfig()
