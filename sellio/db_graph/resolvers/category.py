from collections import defaultdict

from hiku.engine import pass_context
from hiku.graph import Field
from sqlalchemy import and_
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.models.category import Category


@pass_context
async def resolve_child_category_ids(
    ctx: TGraphContext, _: list[Field], category_ids: list[int]
):
    query = select(Category.id, Category.parent_category_id).where(
        and_(
            Category.parent_category_id.in_(category_ids),
        )
    )
    async with ctx["db.session_async"].session() as session:
        result = await session.execute(query)

    mapping = defaultdict(list)
    for row in result:
        mapping[row.parent_category_id].append(row.id)

    return [[mapping[category_id]] for category_id in category_ids]
