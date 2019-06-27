"""create database, schema and tables

Revision ID: 306a5eeb0073
Revises: 3dcae3eb8267
Create Date: 2019-04-16 10:37:59.389211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from catalog.config import source


# revision identifiers, used by Alembic.
revision = "306a5eeb0073"
down_revision = "3dcae3eb8267"
branch_labels = None
depends_on = None


def upgrade():
    # create database
    conn = op.get_bind()
    conn.execution_options(isolation_level="AUTOCOMMIT")

    engine = sa.create_engine(source["engine"])

    conn_sa = engine.connect()

    cursor = conn_sa.connection.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}'".format(source["db"]))

    exists = cursor.fetchone()
    if not exists:
        op.execute("create database {} owner {}".format(source["db"], source["user"]))

    # create schema
    conn.execute("create schema if not exists {} AUTHORIZATION {}".format(source["schema"], source["user"]))

    # create tables
    inspector = inspect(conn)
    tables = inspector.get_table_names(schema=source["schema"])

    if "cardio_administration" not in tables:
        op.create_table("cardio_administration",
                        sa.Column("id", sa.Integer(), nullable=False),
                        sa.Column("subject_id", sa.Integer(), nullable=True),
                        sa.Column("latest_admittime", sa.DateTime(), nullable=True),
                        sa.Column("urgent", sa.Integer(), nullable=True),
                        sa.Column("emergency", sa.Integer(), nullable=True),
                        sa.Column("elective", sa.Integer(), nullable=True),
                        sa.Column("newborn", sa.Integer(), nullable=True),
                        sa.Column("count_of_icustay", sa.Integer(), nullable=True),
                        sa.Column("period_of_icustay", sa.Numeric(), nullable=True),
                        sa.PrimaryKeyConstraint("id"),
                        schema=source["schema"]
                        )
    if "cardio_demographic" not in tables:
        op.create_table("cardio_demographic",
                        sa.Column("id", sa.Integer(), nullable=False),
                        sa.Column("subject_id", sa.Integer(), nullable=True),
                        sa.Column("hadm_id", sa.Integer(), nullable=True),
                        sa.Column("admittime", sa.DateTime(), nullable=True),
                        sa.Column("dob", sa.DateTime(), nullable=True),
                        sa.Column("age", sa.Numeric(), nullable=True),
                        sa.Column("gender", sa.String(), nullable=True),
                        sa.Column("insurance", sa.String(), nullable=True),
                        sa.Column("language", sa.String(), nullable=True),
                        sa.Column("religion", sa.String(), nullable=True),
                        sa.Column("marital_status", sa.String(), nullable=True),
                        sa.Column("ethnicity", sa.String(), nullable=True),
                        sa.PrimaryKeyConstraint("id"),
                        schema=source["schema"]
                        )
    if "cardio_labevents" not in tables:
        op.create_table("cardio_labevents",
                        sa.Column("id", sa.Integer(), nullable=False),
                        sa.Column("subject_id", sa.Integer(), nullable=True),
                        sa.Column("hadm_id", sa.Integer(), nullable=True),
                        sa.Column("itemid", sa.Integer(), nullable=True),
                        sa.Column("label", sa.String(), nullable=True),
                        sa.Column("fluid", sa.String(), nullable=True),
                        sa.Column("category", sa.String(), nullable=True),
                        sa.Column("loinc_code", sa.String(), nullable=True),
                        sa.Column("charttime", sa.DateTime(), nullable=True),
                        sa.Column("valuenum", sa.Numeric(), nullable=True),
                        sa.Column("valueuom", sa.String(), nullable=True),
                        sa.PrimaryKeyConstraint("id"),
                        schema=source["schema"]
                        )
    if "cardio_prescription" not in tables:
        op.create_table("cardio_prescription",
                        sa.Column("row_id", sa.Integer(), nullable=False),
                        sa.Column("subject_id", sa.Integer(), nullable=True),
                        sa.Column("hadm_id", sa.Integer(), nullable=True),
                        sa.Column("icustay_id", sa.Integer(), nullable=True),
                        sa.Column("latest_date", sa.DateTime(), nullable=True),
                        sa.Column("drug", sa.String(), nullable=True),
                        sa.Column("drug_group", sa.String(), nullable=True),
                        sa.Column("prod_strength", sa.String(), nullable=True),
                        sa.Column("dose_val_rx", sa.String(), nullable=True),
                        sa.Column("dose_unit_rx", sa.String(), nullable=True),
                        sa.Column("form_val_disp", sa.String(), nullable=True),
                        sa.Column("form_unit_disp", sa.String(), nullable=True),
                        sa.Column("prescription_days", sa.Integer(), nullable=True),
                        sa.PrimaryKeyConstraint("row_id"),
                        schema=source["schema"]
                        )
    if "cardio_procedures" not in tables:
        op.create_table("cardio_procedures",
                        sa.Column("id", sa.Integer(), nullable=False),
                        sa.Column("subject_id", sa.Integer(), nullable=True),
                        sa.Column("hadm_id", sa.Integer(), nullable=True),
                        sa.Column("admittime", sa.DateTime(), nullable=True),
                        sa.Column("procedures", sa.String(), nullable=True),
                        sa.Column("icd9_code", sa.Integer(), nullable=True),
                        sa.PrimaryKeyConstraint("id"),
                        schema=source["schema"]
                        )
    if "d_events" not in tables:
        op.create_table("d_events",
                        sa.Column("event_id", sa.Integer(), nullable=False),
                        sa.Column("category", sa.String(length=100), nullable=True),
                        sa.Column("event_code", sa.String(length=100), nullable=True),
                        sa.Column("event_name", sa.String(length=500), nullable=True),
                        sa.Column("event_unit", sa.String(length=100), nullable=True),
                        sa.Column("standard_code", sa.String(length=100), nullable=True),
                        sa.PrimaryKeyConstraint("event_id"),
                        schema=source["schema"]
                        )
    if "cardio_events" not in tables:
        op.create_table("cardio_events",
                        sa.Column("id", sa.Integer(), nullable=False),
                        sa.Column("subject_id", sa.Integer(), nullable=True),
                        sa.Column("ts", sa.TIMESTAMP(), nullable=True),
                        sa.Column("event_id", sa.Integer(), nullable=True),
                        sa.Column("event_value", sa.String(length=100), nullable=True),
                        sa.ForeignKeyConstraint(["event_id"], ["{}.d_events.event_id".format(source["schema"])], ),
                        sa.PrimaryKeyConstraint("id"),
                        schema=source["schema"]
                        )

    for i in tables:
        conn.execute("ALTER TABLE {}.{} OWNER TO {};".format(source["schema"], i, source["user"]))

    op.execute("grant all on all tables in schema {} to {}".format(source["schema"], source["user"]))


def downgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    tables = inspector.get_table_names(schema=source["schema"])

    for i in tables:
        conn.execute("ALTER TABLE {}.{} OWNER TO postgres;".format(source["schema"], i))
