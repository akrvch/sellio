import inspect
import typing as t

from hiku.executors.asyncio import AsyncIOExecutor
from hiku.extensions.context import CustomContext
from hiku.graph import Graph
from hiku.graph import Root
from hiku.schema import Schema

from sellio.graph.category.links import CategoryLink
from sellio.graph.category.nodes import CategoryNode
from sellio.graph.company.nodes import CompanyNode
from sellio.graph.context import get_graph_context
from sellio.graph.delivery_option.nodes import DeliveryOptionNode
from sellio.graph.menu.links import MenuLink
from sellio.graph.payment_option.nodes import PaymentOptionNode
from sellio.graph.product.links import ProductListLink
from sellio.graph.product.nodes import ProductNode

GRAPH = Graph(
    items=[
        CompanyNode,
        DeliveryOptionNode,
        PaymentOptionNode,
        ProductNode,
        CategoryNode,
        Root([ProductListLink, MenuLink, CategoryLink]),
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


SCHEMA = Schema(
    AsyncIOExecutor(),
    graph=GRAPH,
    extensions=[CustomContext(lambda ec: get_graph_context(ec.context))],
)
