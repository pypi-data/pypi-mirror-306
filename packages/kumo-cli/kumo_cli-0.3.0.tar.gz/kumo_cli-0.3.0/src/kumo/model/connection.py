from typing import Optional

from fabric import Connection


class KumoConnection(Connection):
    def __init__(
        self,
        ssh_host: str,
        ssh_user: str,
        ssh_key: Optional[str] = None,
        ssh_port: Optional[int] = 22,
    ) -> None:
        self.host = ssh_host
        self.user = ssh_user
        self.port = ssh_port
        self.key = ssh_key
        self.connection = None

    def get_connection(self) -> Connection:

        conn_kwargs = {"key_filename": self.key}

        self.connection = {
            "host": self.host,
            "user": self.user,
            "port": self.port,
            "connect_kwargs": conn_kwargs,
        }

        return Connection(**self.connection)
