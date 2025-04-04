"""create category table

Revision ID: 9f456b18fafb
Revises: 885fdd5122ae
Create Date: 2025-03-25 21:30:33.823511

"""

from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f456b18fafb"
down_revision: Union[str, None] = "885fdd5122ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("parent_category_id", sa.Integer(), nullable=True),
        sa.Column("is_adult", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_category_id"],
            ["category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_category_id"), "category", ["id"], unique=True)
    op.create_index(
        op.f("ix_category_parent_category_id"),
        "category",
        ["parent_category_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_category_parent_category_id"), table_name="category")
    op.drop_index(op.f("ix_category_id"), table_name="category")
    op.drop_table("category")
    # ### end Alembic commands ###
