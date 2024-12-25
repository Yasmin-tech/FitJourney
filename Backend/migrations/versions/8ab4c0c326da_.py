"""fix session duration column name

Revision ID: 8ab4c0c326da
Revises: 1dd4cb7a17a7
Create Date: 2024-12-24 23:52:03.415617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8ab4c0c326da'
down_revision = '1dd4cb7a17a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('days', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_session_duration', sa.Integer(), nullable=True))
        batch_op.drop_column('_sesion_duration')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('days', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_sesion_duration', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('_session_duration')

    # ### end Alembic commands ###