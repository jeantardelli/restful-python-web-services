"""empty message

Revision ID: 3636c0406a5c
Revises: 
Create Date: 2020-12-19 14:07:23.966352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3636c0406a5c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=250), nullable=False),
    sa.Column('ttl', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('notification_category_id', sa.Integer(), nullable=False),
    sa.Column('displayed_times', sa.Integer(), server_default='0', nullable=False),
    sa.Column('displayed_once', sa.Boolean(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['notification_category_id'], ['notification_category.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    op.drop_table('notification_category')
    # ### end Alembic commands ###
