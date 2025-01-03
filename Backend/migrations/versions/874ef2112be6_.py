"""empty message

Revision ID: 874ef2112be6
Revises: b1f1a56911c6
Create Date: 2024-12-30 02:52:21.333449

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '874ef2112be6'
down_revision = 'b1f1a56911c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.VARCHAR(length=512),
               type_=sa.String(length=1024),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=1024),
               type_=mysql.VARCHAR(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###