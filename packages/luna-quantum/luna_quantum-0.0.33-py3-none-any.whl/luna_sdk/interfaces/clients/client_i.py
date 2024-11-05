from abc import ABC, abstractmethod

from httpx import Client


class IClient(ABC):
    @property
    @abstractmethod
    def _client(self) -> Client:
        raise NotImplementedError
