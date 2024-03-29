"""Add background_image_id to courses

Revision ID: 8597ea655b85
Revises: a2fe5d8b5530
Create Date: 2022-05-31 13:23:22.424406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8597ea655b85'
down_revision = 'a2fe5d8b5530'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('background_image_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_courses_background_image_id_images'), 'courses', 'images', ['background_image_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_courses_background_image_id_images'), 'courses', type_='foreignkey')
    op.drop_column('courses', 'background_image_id')
    # ### end Alembic commands ###
