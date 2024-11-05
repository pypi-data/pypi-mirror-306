from abc import ABC, abstractmethod


class BaseConfig(ABC):
    def __init__(self, db_host: str, db_port: str, db_user: str, db_pass: str,
                 db_name: str) -> None:
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    @property
    @abstractmethod
    def DATABASE_URL(self) -> str:
        pass

    @property
    @abstractmethod
    def session(self):
        pass
