"""Add rank columns to like tables

Revision ID: 97bcbbf84230
Revises: 23463617c2dc
Create Date: 2025-05-15 10:04:22.774806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97bcbbf84230'
down_revision = '23463617c2dc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('waifu_like', sa.Column('w_rank', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('husbando_like', sa.Column('h_rank', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('other_like', sa.Column('o_rank', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('waifu_like', 'w_rank')
    op.drop_column('husbando_like', 'h_rank')
    op.drop_column('other_like', 'o_rank')