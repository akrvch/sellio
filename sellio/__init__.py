from threading import RLock
from typing import Any

GLOBAL_STORAGE_KEY_TEMPLATE = "GlobalStorageProxy_{}"


class GlobalStorage:
    _storage = {}
    _lock = RLock()
    _key_template = GLOBAL_STORAGE_KEY_TEMPLATE

    def _key(self, key: str) -> str:
        return self._key_template.format(key)

    def _set(self, key: str, value: Any) -> None:
        key_ = self._key(key)
        if key_ in self._storage:
            raise RuntimeError(f"'{key}' already configured")
        with self._lock:
            self._storage[key_] = value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._set(key, value)

    def _get(self, key: str) -> Any:
        try:
            return self._storage[self._key(key)]
        except KeyError:
            raise RuntimeError(f"'{key}' not configured")

    def get(self, key: str) -> Any:
        with self._lock:
            return self._get(key)


global_storage = GlobalStorage()


class GlobalProxy:
    def __init__(self, key: str):
        self._key = key

    def __repr__(self) -> str:
        return self.__value__().__repr__()

    def __str__(self) -> str:
        return self.__value__().__str__()

    def __dir__(self) -> list[str]:
        return self.__value__().__dir__()

    def __hash__(self) -> int:
        return self.__value__().__hash__()

    def __getattr__(self, item: str) -> Any:
        return self.__value__().__getattribute__(item)

    def __value__(self) -> Any:
        return global_storage.get(self._key)
