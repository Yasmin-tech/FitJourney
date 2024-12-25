"""empty message

Revision ID: 5630e9076353
Revises: 478929920e74
Create Date: 2024-12-25 10:37:49.067133

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5630e9076353'
down_revision = '478929920e74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_difficulty', sa.Integer(), nullable=False))
        batch_op.drop_column('difficulty')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('difficulty', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('_difficulty')

    # ### end Alembic commands ###