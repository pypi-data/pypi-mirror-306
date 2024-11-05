from typing import Dict, Optional, Type

from pydantic import BaseModel

from luna_sdk.schemas.solver_parameters.aws import QaoaParameters as AwsQaoaParameters
from luna_sdk.schemas.solver_parameters.dwave import (
    DialecticSearchParameters,
    KerberosParameters,
    LeapHybridBqmParameters,
    LeapHybridCqmParameters,
    ParallelTemperingParameters,
    ParallelTemperingQpuParameters,
    PopulationAnnealingParameters,
    PopulationAnnealingQpuParameters,
    QAGAParameters,
    QbSolvLikeQpuParameters,
    QbSolvLikeSimulatedAnnealingParameters,
    QbSolvLikeTabuSearchParameters,
    QuantumAnnealingParameters,
    RepeatedReverseQuantumAnnealingParameters,
    RepeatedReverseSimulatedAnnealingParameters,
    SAGAParameters,
    SimulatedAnnealingParameters,
    TabuSearchParameters,
)
from luna_sdk.schemas.solver_parameters.fujitsu import (
    DigitalAnnealerCPUParameters,
    DigitalAnnealerV2Parameters,
    DigitalAnnealerV3Parameters,
)
from luna_sdk.schemas.solver_parameters.ibm import VqeParameters
from luna_sdk.schemas.solver_parameters.ibm import QaoaParameters as IbmQaoaParameters
from luna_sdk.schemas.solver_parameters.qctrl import (
    QaoaParameters as QctrlQaoaParameters,
)

_provider_solver_param_dict: Dict[str, Dict[str, Optional[Type[BaseModel]]]] = {
    "aws": {
        "QAOA": AwsQaoaParameters,
    },
    "dwave": {
        "BF": None,
        "DS": DialecticSearchParameters,
        "K": KerberosParameters,
        "LBQM": LeapHybridBqmParameters,
        "LCQM": LeapHybridCqmParameters,
        "PT": ParallelTemperingParameters,
        "PTQ": ParallelTemperingQpuParameters,
        "PA": PopulationAnnealingParameters,
        "PAQ": PopulationAnnealingQpuParameters,
        "QLQ": QbSolvLikeQpuParameters,
        "QLSA": QbSolvLikeSimulatedAnnealingParameters,
        "QLTS": QbSolvLikeTabuSearchParameters,
        "QA": QuantumAnnealingParameters,
        "RRQA": RepeatedReverseQuantumAnnealingParameters,
        "RRSA": RepeatedReverseSimulatedAnnealingParameters,
        "SA": SimulatedAnnealingParameters,
        "TS": TabuSearchParameters,
        "SAGA": SAGAParameters,
        "SAGAPW": None,
        "SAGAMP": None,
        "QAGA": QAGAParameters,
        "QAGAPW": None,
        "QAGAMP": None,
    },
    "fujitsu": {
        "DACPU": DigitalAnnealerCPUParameters,
        "DAV3": DigitalAnnealerV3Parameters,
        "DAV2": DigitalAnnealerV2Parameters,
    },
    "ibm": {
        "QAOA": IbmQaoaParameters,
        "VQE": VqeParameters,
    },
    "qctrl": {
        "QCTRLQAOA": QctrlQaoaParameters,
    },
    "zib": {
        "SCIP": None,
    },
}


def get_parameter_by_solver(solver: str, provider: str) -> Optional[Type[BaseModel]]:
    if provider not in _provider_solver_param_dict:
        return None

    if solver not in _provider_solver_param_dict[provider]:
        return None
    return _provider_solver_param_dict[provider][solver]
