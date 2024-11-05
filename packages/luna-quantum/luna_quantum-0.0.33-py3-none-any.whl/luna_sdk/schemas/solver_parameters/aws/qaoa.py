from typing import List, Optional

from pydantic import Field

from luna_sdk.schemas.solver_parameters.aws.optimizer_params import OptimizerParams
from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter


class QaoaParameters(BaseParameter):
    """
    The Quantum Approximate Optimization Algorithm ([QAOA](https://arxiv.org/abs/1411.4028))
    solves combinatorial optimization problems by approximating the solution.

    The Quantum Approximate Optimization Algorithm (QAOA) belongs to the class of hybrid quantum algorithms
    (leveraging both classical as well as quantum compute), that are widely believed to be the working horse
    for the current NISQ (noisy intermediate-scale quantum) era. In this NISQ era QAOA is also an emerging
    approach for benchmarking quantum devices and is a prime candidate for demonstrating a practical
    quantum speed-up on near-term NISQ device.

    Parameters
    ----------
    aws_provider: str
        QPU provider name from Amazon Braket.
        Available providers and devices can be found
        [here](https://us-east-1.console.aws.amazon.com/braket/home?region=us-east-1#/devices).

    aws_device: str
       QPU device name from Amazon Braket.
       Available providers and devices can be found
       [here](https://us-east-1.console.aws.amazon.com/braket/home?region=us-east-1#/devices).

    seed: Optional[int]
        Seed for the random number generator. Default: 385920.

    reps: Optional[int]
        The number of repetitions in the QAOA circuit. Default: 1.

    initial_values: Optional[List[float]]
        Initial values for the QAOA parameters. Default: None.

    shots: int
        The number of shots to run on the quantum device. Default: 1024.

    optimizer_params: Optional[dict]
        Parameters for the optimizer. Default: None.

    All possible optimizer parameters can be found in the [scipy.optimize.minimize documentation](https://docs.scipy.org/doc/scipy-1.13.1/reference/generated/scipy.optimize.minimize.html).
    """

    aws_provider: str = ""
    aws_device: str = ""
    seed: Optional[int] = 385920
    reps: Optional[int] = 1
    initial_values: Optional[List[float]] = None
    shots: Optional[int] = 1024
    optimizer_params: OptimizerParams = OptimizerParams()
