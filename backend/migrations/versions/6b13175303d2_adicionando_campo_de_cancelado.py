"""Adicionando campo de cancelado

Revision ID: 6b13175303d2
Revises: 4d7163e8ab0b
Create Date: 2026-10-27 00:26:37.360224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b13175303d2'
down_revision: Union[str, Sequence[str], None] = '4d7163e8ab0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE status_leilao ADD VALUE 'cancelado'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
