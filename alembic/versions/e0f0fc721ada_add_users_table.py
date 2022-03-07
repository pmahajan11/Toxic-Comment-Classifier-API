"""add users table

Revision ID: e0f0fc721ada
Revises: 270e5b317ddf
Create Date: 2022-03-06 19:28:06.931445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f0fc721ada'
down_revision = '270e5b317ddf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                             sa.Column("email", sa.String(), nullable=False, unique=True),
                             sa.Column("password", sa.String(), nullable=False),
                             sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()')))
    pass


def downgrade():
    op.drop_table("users")
    pass
