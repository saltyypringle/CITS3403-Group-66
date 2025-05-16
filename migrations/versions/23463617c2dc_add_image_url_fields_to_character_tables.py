"""Add image_url fields to character tables

Revision ID: 23463617c2dc
Revises: fda7353c5cc0
Create Date: 2025-05-12 09:56:49.255340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23463617c2dc'
down_revision = 'fda7353c5cc0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('waifu', sa.Column('image_url', sa.String(length=200), nullable=True))
    op.add_column('husbando', sa.Column('image_url', sa.String(length=200), nullable=True))
    op.add_column('other', sa.Column('image_url', sa.String(length=200), nullable=True))
    op.add_column('waifu_check', sa.Column('image_url', sa.String(length=200), nullable=True))
    op.add_column('husbando_check', sa.Column('image_url', sa.String(length=200), nullable=True))
    op.add_column('other_check', sa.Column('image_url', sa.String(length=200), nullable=True))

    # Add extra fields to waifu_check
    op.add_column('waifu_check', sa.Column('submission_date', sa.DateTime(), nullable=True))
    op.add_column('waifu_check', sa.Column('status', sa.String(length=20), nullable=True, server_default='Pending'))
    op.add_column('waifu_check', sa.Column('mod_notes', sa.Text(), nullable=True))

    # Add extra fields to husbando_check
    op.add_column('husbando_check', sa.Column('submission_date', sa.DateTime(), nullable=True))
    op.add_column('husbando_check', sa.Column('status', sa.String(length=20), nullable=True, server_default='Pending'))
    op.add_column('husbando_check', sa.Column('mod_notes', sa.Text(), nullable=True))

    # Add extra fields to other_check
    op.add_column('other_check', sa.Column('submission_date', sa.DateTime(), nullable=True))
    op.add_column('other_check', sa.Column('status', sa.String(length=20), nullable=True, server_default='Pending'))
    op.add_column('other_check', sa.Column('mod_notes', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('waifu', 'image_url')
    op.drop_column('husbando', 'image_url')
    op.drop_column('other', 'image_url')
    op.drop_column('waifu_check', 'image_url')
    op.drop_column('husbando_check', 'image_url')
    op.drop_column('other_check', 'image_url')

    # Remove extra fields from waifu_check
    op.drop_column('waifu_check', 'submitted_by')
    op.drop_column('waifu_check', 'submission_date')
    op.drop_column('waifu_check', 'status')
    op.drop_column('waifu_check', 'mod_notes')

    # Remove extra fields from husbando_check
    op.drop_column('husbando_check', 'submitted_by')
    op.drop_column('husbando_check', 'submission_date')
    op.drop_column('husbando_check', 'status')
    op.drop_column('husbando_check', 'mod_notes')

    # Remove extra fields from other_check
    op.drop_column('other_check', 'submitted_by')
    op.drop_column('other_check', 'submission_date')
    op.drop_column('other_check', 'status')
    op.drop_column('other_check', 'mod_notes')
