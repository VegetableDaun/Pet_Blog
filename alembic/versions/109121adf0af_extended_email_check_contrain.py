"""Extended email check contrain

Revision ID: 109121adf0af
Revises: 21b059b41c65
Create Date: 2025-07-21 15:59:43.886347

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "109121adf0af"
down_revision: Union[str, None] = "21b059b41c65"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        constraint_name="check_email_users", table_name="users", type_="check"
    )

    op.create_check_constraint(
        condition="email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
        constraint_name="check_email_users",
        table_name="users",
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="check_email_users", table_name="users", type_="check"
    )

    op.create_check_constraint(
        condition="email ~ '^[A-Za-z0-9]+@[A-Za-z0-9]+\\.[A-Za-z0-9]+$'",
        constraint_name="check_email_users",
        table_name="users",
    )
