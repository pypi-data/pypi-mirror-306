from typing import Literal, Optional, Tuple, Union

from pydantic import ConfigDict, Field

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter
from luna_sdk.schemas.solver_parameters.fujitsu.partial_config import PartialConfig


class CommonParams(BaseParameter):
    auto_tuning: Literal[
        "NOTHING",
        "SCALING",
        "AUTO_SCALING",
        "SAMPLING",
        "AUTO_SCALING_AND_SAMPLING",
        "SCALING_AND_SAMPLING",
    ] = "NOTHING"
    scaling_factor: Union[int, float] = 1.0
    scaling_bit_precision: int = 64
    guidance_config: Optional[PartialConfig] = None
    random_seed: Optional[int] = Field(default=None, ge=0, le=9_999)
    timeseries_max_bits: Optional[int] = None
    solver_max_bits: int = 2**13

    model_config = ConfigDict(arbitrary_types_allowed=True)


class V2Params(BaseParameter):
    optimization_method: Literal["annealing", "parallel_tempering"] = "annealing"
    temperature_start: float = Field(default=1_000.0, ge=0.0, le=1e20)
    temperature_end: float = Field(default=1.0, ge=0.0, le=1e20)
    temperature_mode: int = 0
    temperature_interval: int = Field(default=100, ge=1, le=int(1e20))
    offset_increase_rate: float = Field(default=5.0, ge=0.0, le=1e20)
    solution_mode: Literal["QUICK", "COMPLETE"] = "COMPLETE"
    flip_probabilities: Tuple[float, float] = 0.99, 0.01
    annealing_steps: Tuple[float, float] = 0.0, 0.5
    sampling_runs: int = 100


class ConnectionParams(BaseParameter):
    annealer_protocol: Literal["http", "https"] = "https"
    annealer_address: str = "cloud.ts.fujitsu.com"
    annealer_port: int = Field(default=443, ge=0, le=2**16)
    annealer_path: str = "/da-s"
    request_mode: Literal["stream", "simple", "gzip"] = "simple"
    annealer_queue_size: int = 16
    timeout: int = 1_800
