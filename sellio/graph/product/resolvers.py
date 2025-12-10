from hiku.engine import pass_context
from hiku.graph import Nothing
from hiku.graph import NothingType
from sqlalchemy import exists
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.models.product import Product


async def link_products_list(opts: dict[str, list[int]]) -> list[int]:
    return opts["productIds"]


@pass_context
async def link_product_view(
    ctx: TGraphContext, opts: dict[str, int]
) -> int | NothingType:
    product_id = opts["id"]

    async with ctx["db.session_async"].session() as session:
        product_exists = (
            await session.execute(
                select(exists().where(Product.id == product_id))
            )
        ).scalar_one()

    if not product_exists:
        return Nothing

    return product_id
