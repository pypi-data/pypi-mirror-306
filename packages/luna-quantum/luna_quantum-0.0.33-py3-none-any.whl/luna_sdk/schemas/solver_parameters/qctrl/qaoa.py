from typing import Any, Optional

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class QaoaParameters(BaseParameter):
    """
    QAOA is a popular algorithm that can be applied to a wide range of optimization problems that are out of reach today
    like portfolio optimization, efficient logistics routing, and asset liability management.

    This version of QAOA is from Q-CTRL's software framework “Fire Opal”.
    When running QAOA via Fire Opal, all aspects of running QAOA on real hardware are
    fully optimized to reduce errors and improve the quality of solutions. By tailoring all parts of the algorithm to be hardware-optimized,
    Fire Opal enables larger problems to converge on the correct solution and do so in fewer iterations, reducing the required execution time.

    For further information, see Q-CTRL's documentation(https://docs.q-ctrl.com/fire-opal/topics/fire-opals-qaoa-solver).

    Parameters
    ----------
    ### organization_slug: str | None
        Organization slug from the organization of the user. Required, if the user is part of more than one organization.
        This information can be retrieved from your Q-CTRL account. Default: None

    ### backend_name: str
        Defines backend simulator for the algorithm.
        To see, which backends are available, please check your ibm account.
        It usually starts with 'ibm_', e.g., 'ibm_osaka'. 'least_busy' is also allowed. In this case, the least busy solver will be used.
        Default: 'basic_simulator'

    ### hub: str
        The IBM Quantum hub. Default: 'ibm-q'

    ### group: str
        The IBM Quantum group. Default: 'open'

    ### project: str
        The IBM Quantum project. Default: 'main'

    ### min_num_vars: int
        Default: 1
    """

    organization_slug: Any = None
    backend_name: Optional[str] = None
    hub: str = "ibm-q"
    group: str = "open"
    project: str = "main"
