"""association table

Revision ID: c8a0e4c8de18
Revises: d12e7399ba32
Create Date: 2023-06-07 20:19:11.871148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a0e4c8de18'
down_revision = 'd12e7399ba32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charity_donations',
    sa.Column('charity_project_id', sa.Integer(), nullable=False),
    sa.Column('donation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['charity_project_id'], ['charityproject.id'], ),
    sa.ForeignKeyConstraint(['donation_id'], ['donation.id'], ),
    sa.PrimaryKeyConstraint('charity_project_id', 'donation_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('charity_donations')
    # ### end Alembic commands ###
