from collections import defaultdict

from hiku.engine import pass_context
from sqlalchemy import and_
from sqlalchemy import select

from sellio.graph import TGraphContext
from sellio.models import DeliveryOption
from sellio.models import PaymentOption


@pass_context
async def link_company_delivery_options(
    ctx: TGraphContext, company_ids: list[int]
):
    query = select(DeliveryOption.id, DeliveryOption.company_id).where(
        and_(
            DeliveryOption.company_id.in_(company_ids),
            DeliveryOption.active.is_(True),
        )
    )
    async with ctx["db.session_async"].session() as session:
        result = await session.execute(query)

    mapping = defaultdict(list)
    for row in result:
        mapping[row.company_id].append(row.id)

    return [mapping.get(company_ids) for company_ids in company_ids]


@pass_context
async def link_company_payment_options(
    ctx: TGraphContext, company_ids: list[int]
):
    query = select(PaymentOption.id, PaymentOption.company_id).where(
        and_(
            PaymentOption.company_id.in_(company_ids),
            PaymentOption.active.is_(True),
        )
    )
    async with ctx["db.session_async"].session() as session:
        result = await session.execute(query)

    mapping = defaultdict(list)
    for row in result:
        mapping[row.company_id].append(row.id)

    return [mapping.get(company_ids) for company_ids in company_ids]
