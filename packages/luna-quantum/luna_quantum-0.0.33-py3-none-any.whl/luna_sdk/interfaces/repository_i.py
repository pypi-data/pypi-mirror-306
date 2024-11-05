from abc import ABC, abstractmethod
from httpx import Client


class IRepository(ABC):
    _client: Client

    def __init__(self, client: Client) -> None:
        self._client = client

    @property
    @abstractmethod
    def _endpoint(self) -> str:
        raise NotImplementedError
