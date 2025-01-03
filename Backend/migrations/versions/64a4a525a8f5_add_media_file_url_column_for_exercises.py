"""add media_file_url column for exercises

Revision ID: 64a4a525a8f5
Revises: 142d303d9f61
Create Date: 2024-12-29 16:43:49.825537

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '64a4a525a8f5'
down_revision = '142d303d9f61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('media_file_url', sa.String(length=255), nullable=True))
        batch_op.drop_column('video_url')
        batch_op.drop_column('img_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img_url', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('video_url', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('media_file_url')

    # ### end Alembic commands ###
