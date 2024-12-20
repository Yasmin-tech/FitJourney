"""test migration, user column has been deleted

Revision ID: 5c8c483d8b6d
Revises: 03e7f0b1c0db
Create Date: 2024-12-20 14:57:42.247878

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c8c483d8b6d'
down_revision = '03e7f0b1c0db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('middle_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('middle_name', mysql.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###