"""init

Revision ID: cb6d9a7d9420
Revises: 9a65c40d318e
Create Date: 2024-11-05 22:28:10.896160

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cb6d9a7d9420'
down_revision: Union[str, None] = '9a65c40d318e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
