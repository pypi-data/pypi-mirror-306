from io import BytesIO
from pathlib import Path

from neowg.key_pair import KeyPair


class WgClientConfig:
    _server_host: str
    _server_pubkey: str
    _ip: str
    _keys: KeyPair
    _used: bool

    def __init__(
            self, ip: str, server_host: str, server_pubkey: str, keys: KeyPair | None = None, used: bool = False
    ) -> None:
        """Создает пользовательский конфиг с указанной связкой ключей или генерирует новую."""
        self._ip = ip
        self._keys = keys or KeyPair()
        self._server_host = server_host
        self._server_pubkey = server_pubkey
        self._used = used

    def dump(self) -> BytesIO:
        """Записывает пользовательский конфиг по указанному пути."""

        file_content = """[Interface]
Address = {client_ip}/32
PrivateKey = {private_key}
DNS = 8.8.8.8

[Peer]
PublicKey = {server_pubkey}
Endpoint = {server_host}
AllowedIPs = 0.0.0.0/0"""
        file_content = file_content.format(
            private_key=self._keys.private_key,
            server_pubkey=self._server_pubkey,
            server_host=self._server_host,
            client_ip=self._ip,
        )

        return BytesIO(file_content.encode())

    def update_keys(self) -> KeyPair:
        """Обновляет ключи в конфиге и помечает его как свободный"""
        new_keys = KeyPair()
        self._keys = new_keys
        self._used = False
        return new_keys

    @property
    def pubkey(self) -> str:
        return self._keys.pubkey

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def private_key(self) -> str:
        return self._keys.private_key

    @property
    def used(self) -> bool:
        return self._used

    def mark_used(self) -> None:
        self._used = True

    def __str__(self) -> str:
        return (f"WgClientConfig(server_host={self._server_host}, server_pubkey={self._server_pubkey}), "
                f"ip={self._ip}, keys={self._keys}, used={self._used})")
