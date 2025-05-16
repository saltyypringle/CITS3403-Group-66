"""Fix forum foreign keys

Revision ID: fda7353c5cc0
Revises: 
Create Date: 2025-05-10 14:15:24.093792

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fda7353c5cc0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # --- USER TABLE ---
    op.create_table('user',
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=64), nullable=False, unique=True),
        sa.Column('email', sa.String(length=120), nullable=False, unique=True),
        sa.Column('password', sa.String(length=200), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # --- WAIFU TABLE ---
    op.create_table('waifu',
        sa.Column('w_char_id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=64), nullable=False),
        sa.Column('last_name', sa.String(length=64)),
        sa.Column('hair_colour', sa.String(length=32)),
        sa.Column('height', sa.Integer()),
        sa.Column('personality', sa.String(length=32)),
        sa.Column('profession', sa.String(length=64)),
        sa.Column('body_type', sa.String(length=32))
    )

    # --- HUSBANDO TABLE ---
    op.create_table('husbando',
        sa.Column('h_char_id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=64), nullable=False),
        sa.Column('last_name', sa.String(length=64)),
        sa.Column('hair_colour', sa.String(length=32)),
        sa.Column('height', sa.Integer()),
        sa.Column('personality', sa.String(length=32)),
        sa.Column('profession', sa.String(length=64)),
        sa.Column('body_type', sa.String(length=32))
    )

    # --- OTHER TABLE ---
    op.create_table('other',
        sa.Column('o_char_id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=64), nullable=False),
        sa.Column('last_name', sa.String(length=64)),
        sa.Column('hair_colour', sa.String(length=32)),
        sa.Column('height', sa.Integer()),
        sa.Column('personality', sa.String(length=32)),
        sa.Column('profession', sa.String(length=64)),
        sa.Column('body_type', sa.String(length=32))
    )

    # --- FORUM POST TABLE ---
    op.create_table('forum_post',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # --- FORUM COMMENT TABLE ---
    op.create_table('forum_comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['forum_post.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # --- WAIFU_CHECK TABLE ---
    op.create_table('waifu_check',
        sa.Column('wc_id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=50)),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('hair_colour', sa.String(length=50)),
        sa.Column('height', sa.Integer()),
        sa.Column('personality', sa.String(length=10)),
        sa.Column('profession', sa.String(length=100)),
        sa.Column('body_type', sa.String(length=50)),
        sa.Column('submitted_by', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=True)
    )

    # --- HUSBANDO_CHECK TABLE ---
    op.create_table('husbando_check',
        sa.Column('hc_id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=50)),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('hair_colour', sa.String(length=50)),
        sa.Column('height', sa.Integer()),
        sa.Column('personality', sa.String(length=10)),
        sa.Column('profession', sa.String(length=100)),
        sa.Column('body_type', sa.String(length=50)),
        sa.Column('submitted_by', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=True)
    )

    # --- OTHER_CHECK TABLE ---
    op.create_table('other_check',
        sa.Column('oc_id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(length=50)),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('hair_colour', sa.String(length=50)),
        sa.Column('height', sa.Integer()),
        sa.Column('personality', sa.String(length=10)),
        sa.Column('profession', sa.String(length=100)),
        sa.Column('body_type', sa.String(length=50)),
        sa.Column('submitted_by', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=True)
    )

    # --- WAIFU_LIKE TABLE ---
    op.create_table('waifu_like',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
        sa.Column('w_char_id', sa.Integer(), sa.ForeignKey('waifu.w_char_id'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'w_char_id')
    )

    # --- HUSBANDO_LIKE TABLE ---
    op.create_table('husbando_like',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
        sa.Column('h_char_id', sa.Integer(), sa.ForeignKey('husbando.h_char_id'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'h_char_id')
    )

    # --- OTHER_LIKE TABLE ---
    op.create_table('other_like',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
        sa.Column('o_char_id', sa.Integer(), sa.ForeignKey('other.o_char_id'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'o_char_id')
    )

    # --- SHARES TABLE ---
    op.create_table('shares',
        sa.Column('sharer_id', sa.Integer(), sa.ForeignKey('user.user_id'), primary_key=True),
        sa.Column('recipient_id', sa.Integer(), sa.ForeignKey('user.user_id'), primary_key=True)
    )

def downgrade():
    op.drop_table('shares')
    op.drop_table('other_like')
    op.drop_table('husbando_like')
    op.drop_table('waifu_like')
    op.drop_table('other_check')
    op.drop_table('husbando_check')
    op.drop_table('waifu_check')
    op.drop_table('forum_comment')
    op.drop_table('forum_post')
    op.drop_table('other')
    op.drop_table('husbando')
    op.drop_table('waifu')
    op.drop_table('user')