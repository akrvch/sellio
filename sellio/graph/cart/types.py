"""Cart types and enums."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    """Cart item."""

    product_id: int
    name: str
    price: str
    quantity: int


@dataclass(frozen=True)
class Cart:
    """Cart with items."""

    id: int
    company_id: int
    user_id: int | None
    cookie: str | None
    status: int
    created_at: str
    items: tuple[CartItem, ...]
    total_amount: str


@dataclass(frozen=True)
class AddItemResponse:
    """Response for add/update item mutation."""

    cart: Cart | None
    success: bool
    message: str


@dataclass(frozen=True)
class UpdateQuantityResponse:
    """Response for update quantity mutation."""

    cart: Cart | None
    success: bool
    message: str


@dataclass(frozen=True)
class RemoveItemResponse:
    """Response for remove item mutation."""

    cart: Cart | None
    success: bool
    message: str
