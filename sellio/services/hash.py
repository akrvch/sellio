import logging
from abc import ABC
from abc import abstractmethod
from typing import cast

from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import VerifyMismatchError

from sellio import GlobalProxy
from sellio import global_storage

log = logging.getLogger(__name__)


class BaseHasher(ABC):
    @abstractmethod
    def hash(self, string: str) -> str:
        pass

    @abstractmethod
    def verify(self, string: str, hashed_string: str) -> bool:
        pass


class BaseHasherInterface(BaseHasher, ABC): ...


class Argon2Hasher(BaseHasherInterface):
    def __init__(self):
        self._hasher = Argon2PasswordHasher(
            time_cost=3,
            memory_cost=102400,
        )

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        try:
            self._hasher.verify(password_hash, password)
        except VerifyMismatchError:
            return False
        return True


class PasswordHasher(BaseHasher):
    def __init__(self, hasher: BaseHasherInterface):
        self._hasher = hasher

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self._hasher.verify(password_hash, password)


_KEY = "password.hasher"
password_hasher: PasswordHasher = cast(PasswordHasher, GlobalProxy(_KEY))


def init_hasher():
    global_storage.set(
        _KEY,
        PasswordHasher(hasher=Argon2Hasher()),
    )
    log.info("Hasher successfully initialized")
