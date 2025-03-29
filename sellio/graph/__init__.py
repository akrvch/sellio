import re
from typing import Any
from typing import Sequence
from typing import TypedDict

from hiku.graph import Field
from hiku.graph import Nothing

from sellio.services.db import DatabaseSessionManager

type Contexts = Sequence[Any]
type Fields = Sequence[Field]

camel_to_snake_case_re = re.compile(r"(?<!^)(?=[A-Z])")

TGraphContext = TypedDict(
    "TGraphContext",
    {
        "db.session_async": DatabaseSessionManager,
    },
)


def direct_link(contexts: Contexts) -> Contexts:
    return contexts


def maybe_direct_link(contexts: Sequence[Any]) -> Contexts:
    return [context if context is not None else Nothing for context in contexts]


class UniversalMapper:
    def __init__(self, node_name: str):
        self._node_name = node_name

    def __call__(self, fields: Fields, contexts: list[Any]) -> list[list[Any]]:
        return [
            [self._get_field(f.name, context) for f in fields]
            for context in contexts
        ]

    def _get_field(self, field_name: str, context: Any) -> Any:
        snake_field_name = camel_to_snake_case_re.sub(r"_", field_name).lower()

        for name in (
            snake_field_name,
            snake_field_name.lstrip("_"),
        ):
            try:
                return getattr(context, name)
            except AttributeError:
                pass

        try:
            return getattr(context, field_name)
        except AttributeError as e:
            e.add_note(f"Error occurred in node '{self._node_name}'")
            raise e
