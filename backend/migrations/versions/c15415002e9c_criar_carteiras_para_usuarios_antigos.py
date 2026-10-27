"""Criar carteiras para usuarios antigos

Revision ID: c15415002e9c
Revises: 71fbfd98eda7
Create Date: 2026-10-25 01:56:25.011875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c15415002e9c'
down_revision: Union[str, Sequence[str], None] = '71fbfd98eda7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    INSERT INTO carteiras (usuario_id, saldo,saldo_reservado)
    SELECT u.id ,0.00,0.00
    FROM usuarios as  u
    WHERE NOT EXISTS(
    SELECT 1 
    FROM carteiras c
    WHERE c.usuario_id = u.id
    )
     ON CONFLICT (usuario_id) DO NOTHING
    
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
