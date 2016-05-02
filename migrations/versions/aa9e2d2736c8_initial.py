"""initial

Revision ID: aa9e2d2736c8
Revises: None
Create Date: 2016-04-29 12:52:02.084682

"""

# revision identifiers, used by Alembic.
revision = 'aa9e2d2736c8'
down_revision = None

from alembic import op
import sqlalchemy as sa

import app.utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.Unicode(length=256), nullable=False),
    sa.Column('doc_repo', sa.String(length=256), nullable=False),
    sa.Column('title', sa.Unicode(length=256), nullable=False),
    sa.Column('root_domain', sa.String(length=256), nullable=False),
    sa.Column('root_fastly_domain', sa.String(length=256), nullable=False),
    sa.Column('bucket_name', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('builds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_ended', sa.DateTime(), nullable=True),
    sa.Column('git_refs', app.utils.JSONEncodedVARCHAR(length=2048), nullable=True),
    sa.Column('github_requester', sa.String(length=256), nullable=True),
    sa.Column('uploaded', sa.Boolean(), nullable=True),
    sa.Column('surrogate_key', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_builds_product_id'), 'builds', ['product_id'], unique=False)
    op.create_table('editions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('build_id', sa.Integer(), nullable=True),
    sa.Column('tracked_refs', app.utils.JSONEncodedVARCHAR(length=2048), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=False),
    sa.Column('title', sa.Unicode(length=256), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_rebuilt', sa.DateTime(), nullable=False),
    sa.Column('date_ended', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['build_id'], ['builds.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_editions_build_id'), 'editions', ['build_id'], unique=False)
    op.create_index(op.f('ix_editions_product_id'), 'editions', ['product_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_editions_product_id'), table_name='editions')
    op.drop_index(op.f('ix_editions_build_id'), table_name='editions')
    op.drop_table('editions')
    op.drop_index(op.f('ix_builds_product_id'), table_name='builds')
    op.drop_table('builds')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('products')
    ### end Alembic commands ###