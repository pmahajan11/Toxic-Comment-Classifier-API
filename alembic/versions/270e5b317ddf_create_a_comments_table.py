"""create a comments table

Revision ID: 270e5b317ddf
Revises: 
Create Date: 2022-03-06 19:08:56.501719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '270e5b317ddf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("comments", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                               sa.Column("comment_text", sa.String(), nullable=False),
                               sa.Column("toxic_score", sa.Float(), nullable=False),
                               sa.Column("evaluated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()')))
    pass


def downgrade():
    op.drop_table("comments")
    pass
