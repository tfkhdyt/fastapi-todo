"""create tasks table

Revision ID: 73bf43c545b8
Revises:
Create Date: 2025-05-29 12:38:19.686622

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "73bf43c545b8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("done", sa.Boolean, nullable=False, default=False),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
    pass
