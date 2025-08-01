"""Added Bcrypt for passwords So Changed constrain for the password field in DB

Revision ID: fb232b1a37a1
Revises: eff1fade4726
Create Date: 2025-06-24 17:41:33.513007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb232b1a37a1'
down_revision: Union[str, None] = 'eff1fade4726'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(),
        type_=sa.String(length=72),
        existing_nullable=False,
        schema="dev",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=72),
        type_=sa.String(),
        existing_nullable=False,
        schema="dev",
    )
    # ### end Alembic commands ###
