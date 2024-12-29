"""delete img and video url column and only have one media type to upload

Revision ID: 142d303d9f61
Revises: 5630e9076353
Create Date: 2024-12-28 01:32:26.936132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '142d303d9f61'
down_revision = '5630e9076353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('custom_exercises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('media_file_url', sa.String(length=255), nullable=True))
        batch_op.drop_column('img_url')
        batch_op.drop_column('video_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('custom_exercises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('video_url', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('img_url', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('media_file_url')

    # ### end Alembic commands ###
