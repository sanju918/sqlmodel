"""Moving is_active to user table

Revision ID: 91c26c74feee
Revises: 023b8afe1c1b
Create Date: 2023-09-12 17:58:13.002180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "91c26c74feee"
down_revision: Union[str, None] = "023b8afe1c1b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profiles", "is_active")
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_active")
    op.add_column(
        "profiles",
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
