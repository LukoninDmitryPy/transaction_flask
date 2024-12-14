"""empty message

Revision ID: 00a538680c6d
Revises: b208c8296709
Create Date: 2024-12-14 07:35:03.822942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00a538680c6d'
down_revision: Union[str, None] = 'b208c8296709'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
