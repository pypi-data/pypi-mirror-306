from abc import abstractmethod, ABC


class ConnectorInterface(ABC):

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _disconnect(self):
        pass

    @abstractmethod
    def _disconnect(self):
        pass

    @abstractmethod
    def load(self, collection_name: str, msg: dict) -> any:
        pass

    @abstractmethod
    def bulk_load(self, collection_name: str, msg: list[dict]) -> any:
        pass
