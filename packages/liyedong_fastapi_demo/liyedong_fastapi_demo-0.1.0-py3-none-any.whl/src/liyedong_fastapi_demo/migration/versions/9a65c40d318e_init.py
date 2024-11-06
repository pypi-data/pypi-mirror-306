"""init

Revision ID: 9a65c40d318e
Revises: 5ff0288db228
Create Date: 2024-11-05 22:21:01.921850

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9a65c40d318e'
down_revision: Union[str, None] = '5ff0288db228'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
