import inspect
import typing as t

from hiku.enum import Enum
from hiku.executors.asyncio import AsyncIOExecutor
from hiku.extensions.context import CustomContext
from hiku.graph import Graph
from hiku.graph import Root
from hiku.scalar import Date
from hiku.schema import Schema

from sellio.graph.auth.links import CompleteProfileLink
from sellio.graph.auth.links import LogoutLink
from sellio.graph.auth.links import RequestAuthCodeLink
from sellio.graph.auth.links import UpdateProfileLink
from sellio.graph.auth.links import VerifyAuthCodeLink
from sellio.graph.auth.nodes import CompleteProfileNode
from sellio.graph.auth.nodes import LogoutNode
from sellio.graph.auth.nodes import RequestAuthCodeNode
from sellio.graph.auth.nodes import UpdateProfileNode
from sellio.graph.auth.nodes import VerifyAuthCodeNode
from sellio.graph.auth.types import UpdateProfileErrorCode
from sellio.graph.cart.links import AddItemLink
from sellio.graph.cart.links import RemoveItemLink
from sellio.graph.cart.links import UpdateQuantityLink
from sellio.graph.cart.links import UserCartsLink
from sellio.graph.cart.nodes import AddItemNode
from sellio.graph.cart.nodes import CartItemNode
from sellio.graph.cart.nodes import CartNode
from sellio.graph.cart.nodes import RemoveItemNode
from sellio.graph.cart.nodes import UpdateQuantityNode
from sellio.graph.category.links import CategoryLink
from sellio.graph.category.nodes import CategoryNode
from sellio.graph.company.nodes import CompanyNode
from sellio.graph.context import get_graph_context
from sellio.graph.delivery_info.nodes import DeliveryInfoNode
from sellio.graph.delivery_info.nodes import DeliveryInfoStatusNode
from sellio.graph.delivery_option.nodes import DeliveryOptionNode
from sellio.graph.enums import SortOrder
from sellio.graph.listing_page.nodes import ListingPageNode
from sellio.graph.listings.category.links import CategoryListingLink
from sellio.graph.listings.category.nodes import CategoryListingNode
from sellio.graph.menu.links import MenuLink
from sellio.graph.order.links import CheckoutLink
from sellio.graph.order.links import CreateOrderLink
from sellio.graph.order.links import OrderDetailsLink
from sellio.graph.order.links import OrderListLink
from sellio.graph.order.links import ThankYouPageLink
from sellio.graph.order.nodes import CheckoutPageNode
from sellio.graph.order.nodes import CreateOrderResponseNode
from sellio.graph.order.nodes import OrderNode
from sellio.graph.order.nodes import OrderStatusNode
from sellio.graph.order.nodes import ThankYouPageNode
from sellio.graph.payment_option.nodes import PaymentOptionNode
from sellio.graph.product.links import ProductListLink
from sellio.graph.product.links import ProductViewLink
from sellio.graph.product.nodes import ProductNode
from sellio.graph.user.links import CurrentUserLink
from sellio.graph.user.nodes import UserNode

GRAPH = Graph(
    items=[
        # Base nodes
        CompanyNode,
        DeliveryOptionNode,
        DeliveryInfoNode,
        PaymentOptionNode,
        ProductNode,
        CategoryNode,
        ListingPageNode,
        CategoryListingNode,
        UserNode,
        # Cart nodes
        CartItemNode,
        CartNode,
        # Auth response nodes
        RequestAuthCodeNode,
        VerifyAuthCodeNode,
        CompleteProfileNode,
        UpdateProfileNode,
        LogoutNode,
        # Cart response nodes
        AddItemNode,
        UpdateQuantityNode,
        RemoveItemNode,
        # Order nodes
        OrderNode,
        OrderStatusNode,
        DeliveryInfoStatusNode,
        CheckoutPageNode,
        ThankYouPageNode,
        CreateOrderResponseNode,
        Root(
            [
                ProductListLink,
                ProductViewLink,
                MenuLink,
                CategoryLink,
                CategoryListingLink,
                CurrentUserLink,
                RequestAuthCodeLink,
                VerifyAuthCodeLink,
                CompleteProfileLink,
                UpdateProfileLink,
                LogoutLink,
                UserCartsLink,
                AddItemLink,
                UpdateQuantityLink,
                RemoveItemLink,
                OrderListLink,
                OrderDetailsLink,
                CheckoutLink,
                ThankYouPageLink,
                CreateOrderLink,
            ]
        ),
    ],
    enums=[
        Enum.from_builtin(SortOrder),
        Enum.from_builtin(UpdateProfileErrorCode),
    ],
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
