from abc import ABC
from abc import abstractmethod

from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import VerifyMismatchError

_argon2_hasher = Argon2PasswordHasher(
    time_cost=3,
    memory_cost=102400,
)


class BaseHasher(ABC):
    @staticmethod
    @abstractmethod
    def hash(string: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def verify(string: str, hashed_string: str) -> bool:
        pass


class PasswordHasher(BaseHasher):
    @staticmethod
    def hash(password: str) -> str:
        return _argon2_hasher.hash(password)

    @staticmethod
    def verify(password: str, password_hash: str) -> bool:
        try:
            _argon2_hasher.verify(password_hash, password)
        except VerifyMismatchError:
            return False
        return True
