from enum import Enum, EnumType

from typing import Any

from sqlalchemy import String, Dialect
from sqlalchemy.types import TypeDecorator


class SqlAlEnumDecorator(TypeDecorator):
    impl = String

    def __init__(self, enumcls: EnumType, *args: Any, **kwargs: Any):
        self.enumcls = enumcls
        kwargs.setdefault("length", 50)
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, _: Dialect) -> str | None:
        if value is None:
            return None
        if isinstance(value, self.enumcls):
            return value.name
        return value

    def process_result_value(self, value: str, _: Dialect) -> Enum | None:
        if value is None:
            return None
        return self.enumcls[value]
