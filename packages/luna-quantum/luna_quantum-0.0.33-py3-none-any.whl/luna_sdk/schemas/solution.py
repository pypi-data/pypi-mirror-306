from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from luna_sdk.schemas.enums.solution import SenseEnum
from luna_sdk.schemas.enums.status import StatusEnum
from luna_sdk.schemas.optimization import Optimization
from luna_sdk.schemas.pretty_base import PrettyBase
from luna_sdk.schemas.wrappers import PydanticDatetimeWrapper

Numeric = Union[float, int]
Sample = Dict[str, Numeric]


class Runtime(BaseModel):
    """
    Pydantic model for runtime of a solution.

    Attributes
    ----------
    total: float
        Total time of solution processing
    qpu: Optional[float]
        Total time of the quantum computing processes
    """

    total: float
    qpu: Optional[float]
    # ...


class ConstraintResult(BaseModel):
    satisfied: bool
    extra: Optional[Dict[str, Any]]


class Result(PrettyBase):
    """
    A single result of a solution

    Attributes
    ----------
    sample: List[List[bool]]
        Binary solutions vectors
    energies: List[float]
        Energy corresponding to binary solution vector
    solver: str
        Solver's name
    params: Dict
        Solver params
    runtime: Runtime
        Solution runtime information
    metadata: Optional[Dict]
        Solution's metadata
    """

    sample: Sample
    obj_value: float
    feasible: bool
    constraints: Dict[str, ConstraintResult]


class Solution(PrettyBase):
    """
    The solution class for Solver return values

    Attributes
    ----------
    results: List[List[bool]]
        List of binary solutions vectors
    params: Dict
        Solver params
    runtime: Runtime
        Solution runtime information
    sense: SenseEnum
        Optimization sense, can be 'min' or 'max'.
    metadata: Optional[Dict]
        Solution's metadata
    solver: str
        Solver's name
    provider: str
        The solver provider

    error_message: Optional[str]
        Default is none.
        If an error occurs during the solution process,
        the error message is stored here.
    """

    id: str
    name: Optional[str] = None
    created_date: PydanticDatetimeWrapper
    created_by: str
    modified_date: Optional[PydanticDatetimeWrapper] = None
    modified_by: Optional[str] = None

    error_message: Optional[str] = None
    solver_job_info: Optional[str] = None

    results: Optional[List[Result]]
    params: Dict[str, Any]
    runtime: Optional[Runtime]
    sense: Optional[SenseEnum]
    metadata: Optional[Dict[str, Any]]
    solver: str
    provider: str
    status: StatusEnum
    optimization: Union[Optimization, str]
    representation: Optional[Any] = None

    def __str__(self):
        """Overwrite the default object string representation to use the custom pretty print console representation"""
        data = self.model_dump()
        results = data.pop("results")  # Extract and remove results from data
        metadata = data.pop("metadata")  # Extract and remove metadata from data
        provider = data["provider"]

        divider = "--------------------------------------------------------------------------------\n"

        # Build Meta Data section
        output = f"{divider}META DATA:\n{divider}"
        output += self._pretty_print(data)

        # Build Results section
        if results:
            output += f"\n\n{divider}RESULTS:\n{divider}"
            for i, result in enumerate(results, start=1):
                r = f"Result {i}:\n"
                r += f"    {result}\n"
                output += r
        else:
            output += f"\n\n{divider}RESULTS:\n{divider}"
            output += "    No results..\n"
            output += "    Solution has status: " + str(self.status.value) + "\n"
            if self.error_message:
                output += "    Error message: " + str(self.error_message) + "\n"

        # Build Provider Meta Data section
        output += f"\n\n{divider}{provider.upper()} META DATA:\n{divider}"
        output += (
            self._pretty_print(metadata)
            if metadata
            else "    No metadata from provider..\n"
        )

        return output

    @property
    def head(self):
        """Print a truncated version of the pretty print console representation"""
        limit = 5

        def truncate(data, limit):
            if data is None:
                return None, False

            if isinstance(data, dict):
                d = {
                    k: truncate(v, limit)[0]
                    for i, (k, v) in enumerate(data.items())
                    if i < limit
                }
                return d, len(data) > limit
            elif isinstance(data, list):
                d = data[:limit]
                return d, len(data) > limit
            else:
                return data, False

        data = self.model_dump()
        results = data.pop("results")  # remove results from data
        metadata = data.pop("metadata")  # remove metadata from data
        provider = data["provider"]

        divider = "--------------------------------------------------------------------------------\n"

        # Build Meta Data section
        output = f"{divider}META DATA:\n{divider}"
        output += self._pretty_print(data)

        # Build Results section
        if results:
            output += f"\n\n{divider}RESULTS:\n{divider}"
            output += (
                f"{len(results)} results found. Displaying first {limit} results.\n"
            )
            for i, result in enumerate(results, start=1):
                if i > limit:
                    output += "....\n"
                    break
                r = f"Result {i}:\n"
                r += (
                    f"    {str(result)[:150]}   ....\n"
                    if len(str(result)) > 150
                    else f"    {result}\n"
                )
                output += r
        else:
            output += f"\n\n{divider}RESULTS:\n{divider}"
            output += "    No results..\n"
            output += "    Solution has status: " + str(self.status.value) + "\n"
            if self.error_message:
                output += "    Error message: " + str(self.error_message) + "\n"

        # Build Provider Meta Data section
        metadata_truncated, is_truncated = truncate(metadata, limit)
        output += f"\n\n{divider}{provider.upper()} META DATA"
        output += " (truncated)" if is_truncated else ""
        output += f":\n{divider}"
        output += (
            self._pretty_print(metadata_truncated)
            if metadata
            else "    No metadata from provider..\n"
        )
        output += "...." if is_truncated else ""

        return output


class UseCaseResult(BaseModel):
    representation: Any
    obj_value: float


class UseCaseRepresentation(PrettyBase):
    sense: Optional[SenseEnum]
    results: List[UseCaseResult]
    description: str
