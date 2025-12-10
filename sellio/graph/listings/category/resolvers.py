from typing import Any

from hiku.engine import pass_context
from hiku.graph import Nothing
from hiku.graph import NothingType
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.graph.listing_page.types import ListingPageContext
from sellio.graph.listings.category.types import CategoryListingContext
from sellio.graph.utils import product_sort_order_to_sqlalchemy
from sellio.models.product import Product
from sellio.services.categories import cached_categories


@pass_context
async def resolve_category_listing(
    ctx: TGraphContext, opts: dict[str, Any]
) -> CategoryListingContext | NothingType:
    alias = opts["alias"]
    limit = opts["limit"]
    offset = opts["offset"]
    sort = opts["sort"]

    if not alias:
        return Nothing

    if not (category := cached_categories.get_category_by_alias(alias)):
        print("FUCKING SHET")
        return Nothing

    is_last_level_category = not cached_categories.get_children(category.id)
    product_ids = []

    if is_last_level_category:
        async with ctx["db.session_async"].session() as session:
            query = select(Product.id).where(Product.category_id == category.id)
            if sort:
                query = query.order_by(product_sort_order_to_sqlalchemy(sort))
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            result = await session.execute(query)
            product_ids = result.scalars().all()

    a = CategoryListingContext(
        category_id=category.id,
        page=ListingPageContext(
            product_ids=tuple(product_ids),
        )
        if product_ids
        else None,
    )
    print(a)
    print("FUCK AAAAA")

    return a
