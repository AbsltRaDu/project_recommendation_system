"""empty message

Revision ID: 93d1d1aebe00
Revises: 
Create Date: 2025-05-22 17:42:33.285009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d1d1aebe00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Authors', sa.String(length=100), nullable=False),
    sa.Column('Summary', sa.Text(), nullable=False),
    sa.Column('Rating', sa.Float(), nullable=False),
    sa.Column('Learners', sa.Float(), nullable=False),
    sa.Column('Picture', sa.Text(), nullable=False),
    sa.Column('Link', sa.Text(), nullable=False),
    sa.Column('Category', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('birthdate', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.String(length=20), nullable=False),
    sa.Column('preference', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('click',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recommends',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=100), nullable=False),
    sa.Column('Authors', sa.String(length=100), nullable=False),
    sa.Column('Summary', sa.Text(), nullable=False),
    sa.Column('Rating', sa.Float(), nullable=False),
    sa.Column('Learners', sa.Float(), nullable=False),
    sa.Column('Picture', sa.Text(), nullable=False),
    sa.Column('Link', sa.Text(), nullable=False),
    sa.Column('Category', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('view')
    op.drop_table('recommends')
    op.drop_table('click')
    op.drop_table('users')
    op.drop_table('posts')
    # ### end Alembic commands ###
