"""Add user_id to todos table

Revision ID: 65eb58cac041
Revises: 
Create Date: 2023-07-07 03:01:44.498628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65eb58cac041'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_checked', table_name='users')
    op.drop_index('ix_users_content', table_name='users')
    op.drop_index('ix_users_deadline', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_todos_checked', table_name='todos')
    op.drop_index('ix_todos_content', table_name='todos')
    op.drop_index('ix_todos_deadline', table_name='todos')
    op.drop_index('ix_todos_id', table_name='todos')
    op.drop_table('todos')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deadline', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('checked', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.create_index('ix_todos_id', 'todos', ['id'], unique=False)
    op.create_index('ix_todos_deadline', 'todos', ['deadline'], unique=False)
    op.create_index('ix_todos_content', 'todos', ['content'], unique=False)
    op.create_index('ix_todos_checked', 'todos', ['checked'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('deadline', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('checked', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_deadline', 'users', ['deadline'], unique=False)
    op.create_index('ix_users_content', 'users', ['content'], unique=False)
    op.create_index('ix_users_checked', 'users', ['checked'], unique=False)
    # ### end Alembic commands ###