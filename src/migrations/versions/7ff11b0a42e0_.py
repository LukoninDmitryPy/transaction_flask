"""empty message

Revision ID: 7ff11b0a42e0
Revises: 00a538680c6d
Create Date: 2024-12-14 07:36:06.769591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ff11b0a42e0'
down_revision: Union[str, None] = '00a538680c6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
