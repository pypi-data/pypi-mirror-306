"""init

Revision ID: cbd3d9305678
Revises: cb6d9a7d9420
Create Date: 2024-11-05 22:40:08.659294

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cbd3d9305678'
down_revision: Union[str, None] = 'cb6d9a7d9420'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
