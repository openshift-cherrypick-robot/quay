"""
Add TeamSync table.

Revision ID: be8d1c402ce0
Revises: a6c463dfb9fe
Create Date: 2017-02-23 13:34:52.356812
"""

# revision identifiers, used by Alembic.
revision = "be8d1c402ce0"
down_revision = "a6c463dfb9fe"

import sqlalchemy as sa
from util.migrate import UTF8LongText


def upgrade(op, tables, tester):
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "teamsync",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("transaction_id", sa.String(length=255), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("config", UTF8LongText(), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"], ["loginservice.id"], name=op.f("fk_teamsync_service_id_loginservice")
        ),
        sa.ForeignKeyConstraint(["team_id"], ["team.id"], name=op.f("fk_teamsync_team_id_team")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teamsync")),
    )
    op.create_index("teamsync_last_updated", "teamsync", ["last_updated"], unique=False)
    op.create_index("teamsync_service_id", "teamsync", ["service_id"], unique=False)
    op.create_index("teamsync_team_id", "teamsync", ["team_id"], unique=True)
    ### end Alembic commands ###

    # ### population of test data ### #
    tester.populate_table(
        "teamsync",
        [
            ("team_id", tester.TestDataType.Foreign("team")),
            ("transaction_id", tester.TestDataType.String),
            ("last_updated", tester.TestDataType.DateTime),
            ("service_id", tester.TestDataType.Foreign("loginservice")),
            ("config", tester.TestDataType.JSON),
        ],
    )
    # ### end population of test data ### #


def downgrade(op, tables, tester):
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("teamsync")
    ### end Alembic commands ###
