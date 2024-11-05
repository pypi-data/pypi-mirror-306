from typing import Dict, Optional, Any

from pydantic import BaseModel

from luna_sdk.schemas.rest.qpu_token.token_provider import RestAPITokenProvider


class SolutionIn(BaseModel):
    optimization: str  # id of the optimization
    solver_name: str
    provider: str
    parameters: Dict[str, Any]
    qpu_tokens: Optional[RestAPITokenProvider] = None
    encryption_key: str
    name: Optional[str] = None
