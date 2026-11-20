"""add doreign key to post table

Revision ID: a684cc8f82fc
Revises: 7a30b91e966a
Create Date: 2026-11-20 20:13:58.242954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a684cc8f82fc'
down_revision: Union[str, Sequence[str], None] = '7a30b91e966a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk',table_name="posts",type_="foreignkey")
    op.drop_column('posts','owner_id')

    pass
