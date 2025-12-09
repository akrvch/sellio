import inspect
import typing as t

from hiku.enum import Enum
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
from sellio.graph.enums import SortOrder
from sellio.graph.listing_page.nodes import ListingPageNode
from sellio.graph.listings.category.links import CategoryListingLink
from sellio.graph.listings.category.nodes import CategoryListingNode
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
        ListingPageNode,
        CategoryListingNode,
        Root([ProductListLink, MenuLink, CategoryLink, CategoryListingLink]),
    ],
    enums=[Enum.from_builtin(SortOrder)],
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
