from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel

from luna_sdk.schemas import UseCase

# This works but is kind of ugly.
# In the future, we should find another solution for "dumping" a child of UseCase
# with the name and params.
# OptimizationUseCaseIn can still be created like this:
# opt = OptimizationUseCaseIn(name=name, use_case=use_case)
# Somehow this tricks pydantic into accepting the child of UseCase and adding
# it to the model_dump_json. Without the Generic[UseCase] only the name will be
# added to the model_dump_json

_UseCase = TypeVar("_UseCase", bound=UseCase)


class OptimizationUseCaseIn(BaseModel, Generic[_UseCase]):
    name: str
    use_case: _UseCase
    params: Optional[Dict[str, Any]]
