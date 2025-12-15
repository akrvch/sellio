import logging
from typing import Any

from hiku.engine import pass_context
from hiku.graph import Nothing
from hiku.graph import NothingType
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.graph.cart.types import Cart
from sellio.graph.cart.utils import convert_cart
from sellio.graph.order.types import CheckoutPage
from sellio.graph.order.types import CreateOrderResponse
from sellio.graph.order.types import ThankYouPage
from sellio.models.delivery_info import DeliveryInfo
from sellio.models.delivery_info import DeliveryStatus
from sellio.models.delivery_option import DeliveryOption
from sellio.models.order import Order
from sellio.models.order import OrderStatus
from sellio.models.payment_option import PaymentOption
from sellio.services.cart import CartStatus, cart_service
from sellio.services.session import get_current_user

log = logging.getLogger(__name__)


async def link_order_cart(cart_ids: list[int]) -> list[Cart]:
    """Link cart for order by cart ID."""
    carts = await cart_service.get_carts_by_ids(cart_ids)
    carts_mapping = {cart.id: cart for cart in carts}

    return [convert_cart(carts_mapping[cart_id]) for cart_id in cart_ids]


@pass_context
async def link_order_list(
    ctx: TGraphContext, opts: dict[str, Any]
) -> list[int]:
    current_user = await get_current_user()

    if not current_user:
        return []

    async with ctx["db.session_async"].session() as session:
        query = (
            select(Order.id)
            .where(Order.from_user_id == current_user.id)
            .order_by(Order.date_created.desc())
            .limit(opts["limit"])
            .offset(opts["offset"])
        )
        result = await session.execute(query)
        order_ids = result.scalars().all()

    return order_ids


@pass_context
async def link_order_details(
    ctx: TGraphContext, opts: dict[str, Any]
) -> int | NothingType:
    order_id = opts["id"]
    current_user = await get_current_user()

    if not current_user:
        return Nothing

    async with ctx["db.session_async"].session() as session:
        query = select(Order.id).where(
            Order.id == order_id, Order.from_user_id == current_user.id
        )
        result = await session.execute(query)
        order_id = result.scalar_one_or_none()

    return order_id


@pass_context
async def link_order_delivery_info(
    ctx: TGraphContext, order_ids: list[int]
) -> list[int | NothingType]:
    """Link delivery info for orders."""
    async with ctx["db.session_async"].session() as session:
        query = select(DeliveryInfo.id, DeliveryInfo.order_id).where(
            DeliveryInfo.order_id.in_(order_ids)
        )
        result = await session.execute(query)
        delivery_infos = result.all()

    delivery_info_mapping = {
        delivery_info.order_id: delivery_info.id
        for delivery_info in delivery_infos
    }

    return [
        delivery_info_mapping.get(order_id, Nothing) for order_id in order_ids
    ]


@pass_context
async def query_checkout(
    ctx: TGraphContext, opts: dict[str, Any]
) -> CheckoutPage | NothingType:
    """Get checkout page data."""
    cart_id = opts["cartId"]
    current_user = await get_current_user()

    if not current_user:
        log.warning("Checkout requested but user not authenticated")
        return Nothing

    try:
        # Get cart
        cart = await cart_service.get_cart_by_id(cart_id)

        # Verify cart belongs to user
        if cart.user_id != current_user.id:
            log.warning(
                f"User {current_user.id} attempted to access cart {cart_id} "
                f"belonging to user {cart.user_id}"
            )
            return Nothing

        # Convert cart to Graph type
        cart_obj = convert_cart(cart)

        return CheckoutPage(cart=cart_obj)
    except Exception as e:
        log.error(f"Error getting checkout page: {e}")
        return Nothing


@pass_context
async def query_thank_you_page(
    ctx: TGraphContext, opts: dict[str, Any]
) -> ThankYouPage | NothingType:
    """Get thank you page data."""
    order_id = opts["orderId"]
    current_user = await get_current_user()

    if not current_user:
        log.warning("Thank you page requested but user not authenticated")
        return Nothing

    try:
        async with ctx["db.session_async"].session() as session:
            query = select(Order.id).where(
                Order.id == order_id, Order.from_user_id == current_user.id
            )
            result = await session.execute(query)
            order_id_result = result.scalar_one_or_none()

            if not order_id_result:
                log.warning(
                    f"Order {order_id} not found or doesn't belong to "
                    f"user {current_user.id}"
                )
                return Nothing

        return ThankYouPage(order_id=order_id_result)
    except Exception as e:
        log.error(f"Error getting thank you page: {e}")
        return Nothing


@pass_context
async def mutation_create_order(
    ctx: TGraphContext, opts: dict[str, Any]
) -> CreateOrderResponse:
    """Create order with delivery info."""
    current_user = await get_current_user()

    if not current_user:
        return CreateOrderResponse(
            order_id=None,
            success=False,
            message="User not authenticated",
        )

    try:
        cart_id = opts["cartId"]
        payment_option_id = opts["paymentOptionId"]
        delivery_option_id = opts["deliveryOptionId"]
        comment = opts.get("comment")
        from_first_name = opts["fromFirstName"]
        from_second_name = opts["fromSecondName"]
        from_last_name = opts["fromLastName"]
        from_phone = opts["fromPhone"]
        from_email = opts["fromEmail"]
        city = opts.get("city")
        warehouse = opts.get("warehouse")
        full_delivery_address = opts.get("fullDeliveryAddress")

        # Get cart to verify it exists and get company_id
        cart = await cart_service.get_cart_by_id(cart_id)

        # Verify cart belongs to user
        if cart.user_id != current_user.id:
            return CreateOrderResponse(
                order_id=None,
                success=False,
                message="Cart doesn't belong to current user",
            )

        company_id = cart.company_id

        async with ctx["db.session_async"].session() as session:
            # Verify payment option belongs to company and is active
            payment_option_query = select(PaymentOption).where(
                PaymentOption.id == payment_option_id,
                PaymentOption.company_id == company_id,
                PaymentOption.active.is_(True),
            )
            payment_option_result = await session.execute(payment_option_query)
            payment_option = payment_option_result.scalar_one_or_none()

            if not payment_option:
                return CreateOrderResponse(
                    order_id=None,
                    success=False,
                    message="Invalid or inactive payment option for this company",
                )

            # Verify delivery option belongs to company and is active
            delivery_option_query = select(DeliveryOption).where(
                DeliveryOption.id == delivery_option_id,
                DeliveryOption.company_id == company_id,
                DeliveryOption.active.is_(True),
            )
            delivery_option_result = await session.execute(
                delivery_option_query
            )
            delivery_option = delivery_option_result.scalar_one_or_none()

            if not delivery_option:
                return CreateOrderResponse(
                    order_id=None,
                    success=False,
                    message="Invalid or inactive delivery option for this company",
                )
            # Create order
            order = Order(
                from_user_id=current_user.id,
                from_company_id=cart.company_id,
                from_first_name=from_first_name,
                from_second_name=from_second_name,
                from_last_name=from_last_name,
                from_email=from_email,
                from_phone=from_phone,
                cart_id=cart_id,
                payment_option_id=payment_option_id,
                delivery_option_id=delivery_option_id,
                status=OrderStatus.new,
                comment=comment,
            )
            session.add(order)
            await session.flush()  # Get order.id

            # Create delivery info
            delivery_info = DeliveryInfo(
                order_id=order.id,
                status=DeliveryStatus.init,
                city=city,
                warehouse=warehouse,
                full_delivery_address=full_delivery_address,
            )
            session.add(delivery_info)

            await session.commit()
            await session.refresh(order)

            await cart_service.change_status(cart_id, CartStatus.CHECKED_OUT)
            return CreateOrderResponse(
                order_id=order.id,
                success=True,
                message="Order created successfully",
            )

    except Exception as e:
        log.error(f"Error creating order: {e}")
        return CreateOrderResponse(
            order_id=None,
            success=False,
            message=f"Error creating order: {str(e)}",
        )
