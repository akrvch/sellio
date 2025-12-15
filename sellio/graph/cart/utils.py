from sellio.graph.cart.types import Cart
from sellio.graph.cart.types import CartItem
from sellio.services.cart import CartItemOut
from sellio.services.cart import CartOut


def _convert_cart_item(item: CartItemOut) -> CartItem:
    """Convert cart service item to GraphQL type."""
    return CartItem(
        product_id=item.product_id,
        name=item.name,
        price=item.price,
        quantity=item.quantity,
    )


def convert_cart(cart_out: CartOut) -> Cart:
    """Convert cart service output to GraphQL type."""
    return Cart(
        id=cart_out.id,
        company_id=cart_out.company_id,
        user_id=cart_out.user_id,
        cookie=cart_out.cookie,
        status=cart_out.status,
        created_at=cart_out.created_at,
        items=tuple(_convert_cart_item(item) for item in cart_out.items),
        total_amount=cart_out.total_amount,
    )
