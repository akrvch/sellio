"""Order types and responses."""

from dataclasses import dataclass

from sellio.graph.cart.types import Cart


@dataclass(frozen=True)
class CheckoutPage:
    """Checkout page data."""

    cart: Cart


@dataclass(frozen=True)
class ThankYouPage:
    """Thank you page data."""

    order_id: int


@dataclass(frozen=True)
class CreateOrderResponse:
    """Response for create order mutation."""

    order_id: int | None
    success: bool
    message: str


@dataclass(frozen=True)
class OrderDeliveryOptionContext:
    id: int
    type: str
    name: str


@dataclass(frozen=True)
class OrderPaymentOptionContext:
    id: int
    type: str
    name: str