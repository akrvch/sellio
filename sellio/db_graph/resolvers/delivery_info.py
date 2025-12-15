from hiku.engine import pass_context
from hiku.graph import Field, Nothing
from hiku.graph import NothingType
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.models.delivery_info import DeliveryInfo


@pass_context
async def resolve_order_delivery_info(
    ctx: TGraphContext, _: list[Field], order_ids: list[int]
) -> list[int | NothingType]:
    query = select(DeliveryInfo.id, DeliveryInfo.order_id).where(
        DeliveryInfo.order_id.in_(order_ids)
    )
    async with ctx["db.session_async"].session() as session:
        result = await session.execute(query)

    mapping = {di.order_id: di.id for di in result.all()}

    return [[mapping.get(order_id, Nothing)] for order_id in order_ids]
