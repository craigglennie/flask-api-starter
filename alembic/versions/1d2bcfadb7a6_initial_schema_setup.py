"""initial schema setup

Revision ID: 1d2bcfadb7a6
Revises: None
Create Date: 2013-09-30 14:03:04.503344

"""

# revision identifiers, used by Alembic.
revision = '1d2bcfadb7a6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=True),
        sa.Column('email', sa.String(50), nullable=False, unique=True),
        sa.Column('first_name', sa.Unicode(200), nullable=False),
        sa.Column('last_name', sa.Unicode(200), nullable=True),
    )

    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=True),
        sa.Column('text', sa.Unicode(500), nullable=False),
        sa.Column('is_done', sa.Boolean, nullable=False),
        )


def downgrade():
    pass
