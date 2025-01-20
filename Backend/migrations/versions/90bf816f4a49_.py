"""empty message

Revision ID: 90bf816f4a49
Revises: 2ef67c0dc966
Create Date: 2025-01-20 14:03:33.621896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90bf816f4a49'
down_revision = '2ef67c0dc966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_roles', schema=None) as batch_op:
        batch_op.drop_constraint('user_roles_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('user_roles_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'roles', ['role_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_roles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_roles_ibfk_3', 'users', ['user_id'], ['id'])
        batch_op.create_foreign_key('user_roles_ibfk_2', 'roles', ['role_id'], ['id'])

    # ### end Alembic commands ###
