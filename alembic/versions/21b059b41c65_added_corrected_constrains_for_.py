"""Added Corrected constrains for ArticleSchema

Revision ID: 21b059b41c65
Revises: fb232b1a37a1
Create Date: 2025-06-25 13:56:02.444077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21b059b41c65'
down_revision: Union[str, None] = 'fb232b1a37a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "articles",
        "title",
        existing_type=sa.String(),
        type_=sa.String(length=80),
        existing_nullable=False,
    )

    op.alter_column(
        "articles",
        "content",
        existing_type=sa.String(),
        type_=sa.String(length=280),
        existing_nullable=False,
    )

    op.alter_column(
        "articles",
        "secret_info",
        existing_type=sa.String(),
        type_=sa.String(length=80),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "articles",
        "title",
        existing_type=sa.String(length=80),
        type_=sa.String(),
        existing_nullable=False,
    )

    op.alter_column(
        "articles",
        "content",
        existing_type=sa.String(length=280),
        type_=sa.String(),
        existing_nullable=False,
    )

    op.alter_column(
        "articles",
        "secret_info",
        existing_type=sa.String(length=80),
        type_=sa.String(),
        existing_nullable=False,
    )
