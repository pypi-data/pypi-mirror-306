import json
import os
from typing import Dict, List, Optional

from httpx import Response

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.schemas import QpuTokenOut
from luna_sdk.schemas.create import QpuTokenIn
from luna_sdk.schemas.enums.qpu_token_type import QpuTokenTypeEnum


class QpuTokenRepo(IQpuTokenRepo):
    @property
    def _endpoint(self) -> str:
        return "/qpu-tokens"

    def _get_endpoint_by_type(
        self, token_type: Optional[QpuTokenTypeEnum] = None
    ) -> str:
        if token_type is None:
            return f"{self._endpoint}"
        elif token_type == QpuTokenTypeEnum.PERSONAL:
            return f"{self._endpoint}/private"
        else:
            return f"{self._endpoint}/shared"

    def _get_by_name(
        self, name: str, token_type: QpuTokenTypeEnum, **kwargs
    ) -> QpuTokenOut:
        response: Response = self._client.get(
            f"{self._get_endpoint_by_type(token_type)}/{name}", **kwargs
        )
        response.raise_for_status()

        qpu_token_data = response.json()
        qpu_token_data["token_type"] = token_type
        return QpuTokenOut.model_validate(qpu_token_data)

    def create(
        self,
        name: str,
        provider: str,
        token: str,
        token_type: QpuTokenTypeEnum,
        encryption_key: Optional[str] = None,
        **kwargs,
    ) -> QpuTokenOut:
        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        qpu_token = QpuTokenIn(
            name=name,
            provider=provider,
            token=token,
            encryption_key=encryption_key,
        )

        response: Response = self._client.post(
            self._get_endpoint_by_type(token_type),
            content=qpu_token.model_dump_json(),
            **kwargs,
        )
        response.raise_for_status()
        qpu_token_data = response.json()
        qpu_token_data["token_type"] = token_type
        return QpuTokenOut.model_validate(qpu_token_data)

    def get_all(
        self,
        filter_provider: Optional[str] = None,
        name: Optional[str] = None,
        token_type: Optional[QpuTokenTypeEnum] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> Dict[QpuTokenTypeEnum, List[QpuTokenOut]]:
        params = {}
        if filter_provider:
            params["filter_provider"] = filter_provider

        if name:
            params["name"] = name
        if limit is not None:
            params["limit"] = str(limit)
        if offset is not None:
            params["offset"] = str(offset)

        to_return: Dict[QpuTokenTypeEnum, List[QpuTokenOut]] = {}
        if token_type is None or token_type == QpuTokenTypeEnum.PERSONAL:
            response = self._client.get(
                self._get_endpoint_by_type(QpuTokenTypeEnum.PERSONAL),
                params=params,
                **kwargs,
            )
            response.raise_for_status()
            personal_qpu_tokens = response.json()
            to_return[QpuTokenTypeEnum.PERSONAL] = [
                QpuTokenOut(**qpu_token, token_type=QpuTokenTypeEnum.PERSONAL)
                for qpu_token in personal_qpu_tokens
            ]
        if token_type is None or token_type == QpuTokenTypeEnum.GROUP:
            response = self._client.get(
                self._get_endpoint_by_type(QpuTokenTypeEnum.GROUP),
                params=params,
                **kwargs,
            )
            response.raise_for_status()
            shared_qpu_tokens = response.json()
            to_return[QpuTokenTypeEnum.GROUP] = [
                QpuTokenOut(**qpu_token, token_type=QpuTokenTypeEnum.GROUP)
                for qpu_token in shared_qpu_tokens
            ]

        return to_return

    def get(
        self,
        name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
        **kwargs,
    ) -> QpuTokenOut:
        qpu_token: QpuTokenOut = self._get_by_name(name, token_type, **kwargs)

        return qpu_token

    def rename(
        self, name: str, new_name: str, token_type: QpuTokenTypeEnum, **kwargs
    ) -> QpuTokenOut:
        qpu_token_update_data = {"name": new_name}

        token: QpuTokenOut = self.get(name, token_type)

        response = self._client.patch(
            f"{self._get_endpoint_by_type(token_type)}/{token.name}",
            content=json.dumps(qpu_token_update_data),
            **kwargs,
        )
        response.raise_for_status()

        qpu_token_data = response.json()
        qpu_token_data["token_type"] = token_type
        return QpuTokenOut.model_validate(qpu_token_data)

    def delete(self, name: str, token_type: QpuTokenTypeEnum, **kwargs) -> None:
        response = self._client.delete(
            f"{self._get_endpoint_by_type(token_type)}/{name}", **kwargs
        )
        response.raise_for_status()
