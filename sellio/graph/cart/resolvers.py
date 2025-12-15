"""Cart GraphQL resolvers."""

import logging

from hiku.engine import pass_context
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.graph.cart.types import AddItemResponse
from sellio.graph.cart.types import Cart
from sellio.graph.cart.types import RemoveItemResponse
from sellio.graph.cart.types import UpdateQuantityResponse
from sellio.graph.cart.utils import convert_cart
from sellio.models.product import Product
from sellio.services.cart import AddItemAutoCreateInput
from sellio.services.cart import cart_service
from sellio.services.session import get_current_user

log = logging.getLogger(__name__)


@pass_context
async def query_user_carts(ctx: TGraphContext) -> list[Cart]:
    """Get carts for current authenticated user."""
    # Get current user
    user = await get_current_user()
    if not user:
        log.warning("User carts requested but user not authenticated")
        return []

    try:
        carts = await cart_service.get_carts_by_user(
            user_id=user.id,
            company_id=None,
            status=None,
            limit=50,
            offset=0,
        )
        return [convert_cart(cart) for cart in carts]
    except Exception as e:
        log.error(f"Error getting user carts: {e}")
        return []


@pass_context
async def mutation_add_item(
    ctx: TGraphContext, opts: dict[str, int]
) -> AddItemResponse:
    """Add item to cart. Auto-creates cart if needed. Fetches product details from database."""
    product_id = opts["productId"]

    # Get current user if authenticated
    user = await get_current_user()
    user_id = user.id if user else None

    try:
        # Get product from database
        async with ctx["db.session_async"].session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()

            if not product:
                return AddItemResponse(
                    cart=None,
                    success=False,
                    message=f"Product with ID {product_id} not found",
                )

            # Get company_id from product
            company_id = product.company_id

            # Use discounted price if available, otherwise regular price
            # Check if product has discount through product_discount relationship
            final_price = str(product.price)

            # TODO: In future, calculate discounted price from product.product_discount
            # For now, just use the regular price

        # Add item to cart with quantity = 1 (auto-creates cart if needed)
        input_data = AddItemAutoCreateInput(
            company_id=company_id,
            user_id=user_id,
            cookie=None,  # TODO: Handle anonymous users with cookies
            product_id=product_id,
            name=product.name,
            price=final_price,
            quantity=1,
        )
        cart_out = await cart_service.add_item_auto_create(input_data)
        cart = convert_cart(cart_out)
        return AddItemResponse(
            cart=cart,
            success=True,
            message="Item added successfully",
        )
    except Exception as e:
        log.error(f"Error adding item to cart: {e}")
        return AddItemResponse(
            cart=None,
            success=False,
            message=f"Failed to add item: {str(e)}",
        )


@pass_context
async def mutation_update_quantity(
    ctx: TGraphContext, opts: dict[str, int]
) -> UpdateQuantityResponse:
    """Update item quantity in cart. Finds active cart automatically."""
    product_id = opts["productId"]
    quantity = opts["quantity"]

    # Get current user if authenticated
    user = await get_current_user()
    user_id = user.id if user else None

    try:
        # Get product from database to get company_id
        async with ctx["db.session_async"].session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()

            if not product:
                return UpdateQuantityResponse(
                    cart=None,
                    success=False,
                    message=f"Product with ID {product_id} not found",
                )

            company_id = product.company_id

        # Find active cart for user
        cart_out = await cart_service.get_active_cart(company_id, user_id)
        if not cart_out:
            return UpdateQuantityResponse(
                cart=None,
                success=False,
                message="No active cart found. Please add items first.",
            )

        # Update quantity
        cart_out = await cart_service.update_item_quantity(
            cart_out.id, product_id, quantity
        )
        cart = convert_cart(cart_out)
        return UpdateQuantityResponse(
            cart=cart,
            success=True,
            message="Quantity updated successfully",
        )
    except Exception as e:
        log.error(f"Error updating item quantity: {e}")
        return UpdateQuantityResponse(
            cart=None,
            success=False,
            message=f"Failed to update quantity: {str(e)}",
        )


@pass_context
async def mutation_remove_item(
    ctx: TGraphContext, opts: dict[str, int]
) -> RemoveItemResponse:
    """Remove item from cart. Finds active cart automatically."""
    product_id = opts["productId"]

    # Get current user if authenticated
    user = await get_current_user()
    user_id = user.id if user else None

    try:
        # Get product from database to get company_id
        async with ctx["db.session_async"].session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            product = result.scalar_one_or_none()

            if not product:
                return RemoveItemResponse(
                    cart=None,
                    success=False,
                    message=f"Product with ID {product_id} not found",
                )

            company_id = product.company_id

        # Find active cart for user
        cart_out = await cart_service.get_active_cart(company_id, user_id)
        if not cart_out:
            return RemoveItemResponse(
                cart=None,
                success=False,
                message="No active cart found.",
            )

        # Remove item
        cart_out = await cart_service.remove_item(cart_out.id, product_id)
        cart = convert_cart(cart_out)
        return RemoveItemResponse(
            cart=cart,
            success=True,
            message="Item removed successfully",
        )
    except Exception as e:
        log.error(f"Error removing item from cart: {e}")
        return RemoveItemResponse(
            cart=None,
            success=False,
            message=f"Failed to remove item: {str(e)}",
        )
