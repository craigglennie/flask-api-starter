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
        sa.Column('updated', sa.DateTime, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean, nullable=False, default=False),
        sa.Column('first_name', sa.Unicode(200), nullable=False),
        sa.Column('last_name', sa.Unicode(200), nullable=True),
        sa.Column('confirmed_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'teams',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False),
        sa.Column('name', sa.Unicode(500), nullable=False),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('team_id', sa.Integer, sa.ForeignKey("teams.id"), nullable=False),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False),
        sa.Column('text', sa.Unicode(500), nullable=False),
        sa.Column('is_done', sa.Boolean, nullable=False),
    )

    op.create_table(
        'user_teams',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column('team_id', sa.Integer, sa.ForeignKey("teams.id"), nullable=False),
        sa.UniqueConstraint('team_id', 'user_id'),
    )

def downgrade():
    pass
