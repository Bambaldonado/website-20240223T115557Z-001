"""empty message

Revision ID: 5252db39b520
Revises: 
Create Date: 2024-02-23 16:49:02.980632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5252db39b520'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('supplier', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('supplier')

    # ### end Alembic commands ###
