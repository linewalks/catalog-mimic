"""create user

Revision ID: 3dcae3eb8267
Revises:
Create Date: 2019-04-09 15:56:44.577771

"""
from alembic import op
import sqlalchemy as sa
from catalog.config import source

# revision identifiers, used by Alembic.
revision = "3dcae3eb8267"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    engine = sa.create_engine(source["engine"])

    conn = engine.connect()

    cursor = conn.connection.cursor()

    cursor.execute("SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = '{}'".format(source["user"]))

    exists = cursor.fetchone()
    if not exists:
        op.execute("create role {} login password '{}' CREATEDB CREATEROLE".format(source["user"], source["password"]))

    # ### end Alembic commands ###


def downgrade():
    pass
