"""language

Revision ID: 0c224c621d0f
Revises: 10d3450af02
Create Date: 2018-09-01 17:22:32.360303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c224c621d0f'
down_revision = '10d3450af02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tag', sa.Column('language', sa.String(length=2), nullable=False, server_default='ru'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tag', 'language')
    # ### end Alembic commands ###
