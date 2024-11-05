from typing import Any, Dict, Optional

from pydantic import BaseModel

from luna_sdk.schemas.enums.circuit import CircuitProviderEnum
from luna_sdk.schemas.rest.qpu_token.token_provider import RestAPITokenProvider


class CircuitIn(BaseModel):
    """
    Pydantic model for creation of circuits.

    Attributes
    ----------
    provider: str
        The provider for circuit solving
    provider: ProviderEnum
        The QASM circuit
    params: Dict[str, Any]
        Additional parameters
    encryption_key: str
        Encryption key to be used for encryption of QPU tokens.
    """

    provider: CircuitProviderEnum
    circuit: str
    params: Dict[str, Any] = {}
    qpu_tokens: Optional[RestAPITokenProvider] = None
    encryption_key: str
