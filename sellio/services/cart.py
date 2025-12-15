"""Service for interacting with Sellio Cart REST API."""

from enum import IntEnum
import logging
from typing import Any
from typing import cast

import httpx
from pydantic import BaseModel

from sellio import GlobalProxy
from sellio import global_storage
from sellio.settings import Config

log = logging.getLogger(__name__)


class CartStatus(IntEnum):
    """Cart status."""
    ACTIVE = 1
    LOCKED = 2
    CHECKED_OUT = 3
    CANCELLED = 4


class CartItemIn(BaseModel):
    """Cart item input model."""

    product_id: int
    name: str
    price: str
    quantity: int


class CartItemOut(BaseModel):
    """Cart item output model."""

    product_id: int
    name: str
    price: str
    quantity: int


class CartOut(BaseModel):
    """Cart output model."""

    id: int
    company_id: int
    user_id: int | None
    cookie: str | None
    status: int
    created_at: str
    items: list[CartItemOut]
    total_amount: str


class UpsertCartInput(BaseModel):
    """Input for upserting a cart."""

    company_id: int
    user_id: int | None = None
    cookie: str | None = None


class AddItemAutoCreateInput(BaseModel):
    """Input for adding item with auto-create cart."""

    company_id: int
    user_id: int | None = None
    cookie: str | None = None
    product_id: int
    name: str
    price: str
    quantity: int


class UpdateQuantityInput(BaseModel):
    """Input for updating item quantity."""

    quantity: int


class ChangeStatusInput(BaseModel):
    """Input for changing cart status."""

    status: int


class CartService:
    """Service for interacting with Sellio Cart REST API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    async def _make_request(
        self,
        method: str,
        path: str,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Make HTTP request to cart service."""
        url = f"{self.base_url}{path}"
        try:
            response = await self.client.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            log.error(
                f"Cart service HTTP error: {e.response.status_code} - {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            log.error(f"Cart service request error: {e}")
            raise

    async def get_cart_by_id(self, cart_id: int) -> CartOut:
        """Get cart by ID."""
        data = await self._make_request("GET", f"/api/v1/cart/{cart_id}")
        return CartOut(**data)

    async def get_carts_by_user(
        self,
        user_id: int,
        company_id: int | None = None,
        status: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[CartOut]:
        """Get carts by user with optional filtering."""
        params = {
            "user_id": user_id,
            "limit": limit,
            "offset": offset,
        }
        if company_id is not None:
            params["company_id"] = company_id
        if status is not None:
            params["status"] = status

        data = await self._make_request(
            "GET", "/api/v1/carts/by-user", params=params
        )
        return [CartOut(**item) for item in data]

    async def get_carts_by_ids(self, cart_ids: list[int]) -> list[CartOut]:
        """Get multiple carts by IDs."""
        data = await self._make_request(
            "POST", "/api/v1/carts/by-ids", json_data={"ids": cart_ids}
        )
        return [CartOut(**item) for item in data]

    async def get_active_cart(
        self, company_id: int, user_id: int | None = None
    ) -> CartOut | None:
        """Get active cart for company and user."""
        params = {"company_id": company_id}
        if user_id is not None:
            params["user_id"] = user_id

        try:
            data = await self._make_request(
                "GET", "/api/v1/cart/active", params=params
            )
            return CartOut(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def upsert_cart(self, input_data: UpsertCartInput) -> CartOut:
        """Create new cart or get existing active cart."""
        data = await self._make_request(
            "POST", "/api/v1/cart/upsert", json_data=input_data.model_dump()
        )
        return CartOut(**data)

    async def add_item_auto_create(
        self, input_data: AddItemAutoCreateInput
    ) -> CartOut:
        """Add item to cart (auto-creates cart if needed)."""
        data = await self._make_request(
            "POST", "/api/v1/cart/add-item", json_data=input_data.model_dump()
        )
        return CartOut(**data)

    async def add_or_update_item(
        self, cart_id: int, item: CartItemIn
    ) -> CartOut:
        """Add or update item in existing cart."""
        data = await self._make_request(
            "POST", f"/api/v1/cart/{cart_id}/item", json_data=item.model_dump()
        )
        return CartOut(**data)

    async def update_item_quantity(
        self, cart_id: int, product_id: int, quantity: int
    ) -> CartOut:
        """Update item quantity in cart."""
        data = await self._make_request(
            "PUT",
            f"/api/v1/cart/{cart_id}/item/{product_id}/quantity",
            json_data={"quantity": quantity},
        )
        return CartOut(**data)

    async def remove_item(self, cart_id: int, product_id: int) -> CartOut:
        """Remove item from cart."""
        data = await self._make_request(
            "DELETE", f"/api/v1/cart/{cart_id}/item/{product_id}"
        )
        return CartOut(**data)

    async def change_status(self, cart_id: int, status: CartStatus) -> CartOut:
        """Change cart status."""
        data = await self._make_request(
            "PUT",
            f"/api/v1/cart/{cart_id}/status",
            json_data={"status": status.value},
        )
        return CartOut(**data)

    async def health_check(self) -> dict[str, str]:
        """Check cart service health."""
        return await self._make_request("GET", "/healthz")


_KEY = "cart.service"
cart_service: CartService = cast(CartService, GlobalProxy(_KEY))


def init_cart_service(config: Config):
    """Initialize cart service with config."""
    global_storage.set(_KEY, CartService(config.cart_service_url))
    log.info("Cart service successfully initialized")
