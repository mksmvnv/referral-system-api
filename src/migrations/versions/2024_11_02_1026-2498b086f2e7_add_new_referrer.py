"""Add new referrer

Revision ID: 2498b086f2e7
Revises: 74fe07f0367b
Create Date: 2024-11-02 10:26:43.533298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2498b086f2e7'
down_revision: Union[str, None] = '74fe07f0367b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
