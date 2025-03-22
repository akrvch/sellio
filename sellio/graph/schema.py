import inspect
import typing as t

from hiku.executors.asyncio import AsyncIOExecutor
from hiku.graph import Field
from hiku.graph import Graph
from hiku.graph import Link
from hiku.graph import Node
from hiku.graph import Root
from hiku.schema import Schema
from hiku.types import String
from hiku.types import TypeRef


def mapper(fields: list[Field], contexts: list[t.Any]):
    def _get_field(field_name: str) -> t.Any:
        match field_name:
            case "hello":
                return "world"
        raise AttributeError(f"Field '{field_name}' is not defined")

    return [[_get_field(field.name) for field in fields] for _ in contexts]


def resolver(*args):
    return None


GRAPH = Graph(
    items=[
        Node("HelloWorld", [Field("hello", String, mapper)]),
        Root(
            [
                Link(
                    "helloWorld",
                    TypeRef["HelloWorld"],
                    resolver,
                    requires=None,
                )
            ]
        ),
    ]
)


class AnyIOExecutor(AsyncIOExecutor):
    async def _wrapper(
        self, fn: t.Callable, *args: t.Any, **kwargs: t.Any
    ) -> t.Any:
        result = fn(*args, **kwargs)
        if inspect.isawaitable(result):
            return await result
        else:
            return result

    def submit(self, fn: t.Callable, *args: t.Any, **kwargs: t.Any) -> t.Any:
        return super().submit(self._wrapper, fn, *args, **kwargs)


SCHEMA = Schema(AsyncIOExecutor(), graph=GRAPH)
