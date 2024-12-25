""" change plans table columns names

Revision ID: 6981ae2f9dd7
Revises: 5c8c483d8b6d
Create Date: 2024-12-24 15:24:11.679730

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6981ae2f9dd7'
down_revision = '5c8c483d8b6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_current_weight', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('_target_weight', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('_duration', sa.Integer(), nullable=False))
        batch_op.drop_column('duration')
        batch_op.drop_column('target_weight')
        batch_op.drop_column('current_weight')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plans', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_weight', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('target_weight', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('duration', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('_duration')
        batch_op.drop_column('_target_weight')
        batch_op.drop_column('_current_weight')

    # ### end Alembic commands ###