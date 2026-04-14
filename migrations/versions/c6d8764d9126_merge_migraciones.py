"""merge migraciones

Revision ID: c6d8764d9126
Revises: 027f1187d1f8, eaf7dc325616
Create Date: 2026-04-05 13:14:26.925870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6d8764d9126'
down_revision = ('027f1187d1f8', 'eaf7dc325616')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
