import os
from typing import Any, Dict, Optional

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.circuit_repo_i import ICircuitRepo
from luna_sdk.schemas.circuit import CircuitJob, CircuitResult
from luna_sdk.schemas.create.circuit import CircuitIn
from luna_sdk.schemas.enums.circuit import CircuitProviderEnum
from luna_sdk.schemas.qpu_token import TokenProvider
from luna_sdk.schemas.rest.qpu_token.token_provider import RestAPITokenProvider
from luna_sdk.utils.qpu_tokens import extract_qpu_tokens_from_env


class CircuitRepo(ICircuitRepo):
    _endpoint = "/circuits"

    def create(
        self,
        circuit: str,
        provider: CircuitProviderEnum,
        params: Dict[str, Any] = {},
        qpu_tokens: Optional[TokenProvider] = None,
        encryption_key: Optional[str] = None,
        **kwargs,
    ) -> CircuitJob:
        if qpu_tokens is not None:
            rest_qpu_tokens = RestAPITokenProvider.from_sdk_token_provider(
                TokenProvider.model_validate(qpu_tokens)
            )
        else:
            rest_qpu_tokens = None

        # try to retrieve qpu tokens from env variables
        if rest_qpu_tokens is None:
            rest_qpu_tokens = extract_qpu_tokens_from_env()

        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        circuit_in: CircuitIn = CircuitIn(
            provider=provider,
            circuit=circuit,
            params=params,
            qpu_tokens=rest_qpu_tokens,
            encryption_key=encryption_key,
        )

        response = self._client.post(
            self._endpoint, content=circuit_in.model_dump_json(), **kwargs
        )

        response.raise_for_status()
        return CircuitJob(id=response.json(), provider=provider, params=params)

    def get(
        self,
        job: CircuitJob,
        encryption_key: Optional[str] = None,
        **kwargs,
    ) -> CircuitResult:
        url = f"{self._endpoint}/{job.id}/{job.provider.value}"
        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        if job.params is None:
            job.params = {}
        job.params["encryption_key"] = encryption_key
        response = self._client.get(url, params=job.params, **kwargs)

        response.raise_for_status()
        return CircuitResult.model_validate(response.json())
