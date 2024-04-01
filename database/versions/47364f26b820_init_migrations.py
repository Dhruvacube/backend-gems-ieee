"""init migrations

Revision ID: 47364f26b820
Revises: 
Create Date: 2024-03-31 00:24:52.167107

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "47364f26b820"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_organizations_id", table_name="organizations")
    op.drop_index("ix_organizations_name", table_name="organizations")
    op.drop_index("ix_organizations_role", table_name="organizations")
    op.drop_table("organizations")
    op.drop_index("ix_users_alt_email", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_invite_id", table_name="users")
    op.drop_index("ix_users_name", table_name="users")
    op.drop_index("ix_users_phone", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_sessions_id", table_name="sessions")
    op.drop_index("ix_sessions_token", table_name="sessions")
    op.drop_table("sessions")
    op.drop_index("ix_guests_alt_email", table_name="guests")
    op.drop_index("ix_guests_email", table_name="guests")
    op.drop_index("ix_guests_id", table_name="guests")
    op.drop_index("ix_guests_name", table_name="guests")
    op.drop_index("ix_guests_phone", table_name="guests")
    op.drop_table("guests")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "guests",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("alt_email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("phone", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="guests_pkey"),
    )
    op.create_index("ix_guests_phone", "guests", ["phone"], unique=True)
    op.create_index("ix_guests_name", "guests", ["name"], unique=False)
    op.create_index("ix_guests_id", "guests", ["id"], unique=False)
    op.create_index("ix_guests_email", "guests", ["email"], unique=True)
    op.create_index("ix_guests_alt_email", "guests", ["alt_email"], unique=True)
    op.create_table(
        "sessions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("token", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "valid_till", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="sessions_pkey"),
    )
    op.create_index("ix_sessions_token", "sessions", ["token"], unique=True)
    op.create_index("ix_sessions_id", "sessions", ["id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("alt_email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("phone", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("invite_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("profile_photo", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_phone", "users", ["phone"], unique=True)
    op.create_index("ix_users_name", "users", ["name"], unique=False)
    op.create_index("ix_users_invite_id", "users", ["invite_id"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_alt_email", "users", ["alt_email"], unique=True)
    op.create_table(
        "organizations",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "valid_till", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="organizations_pkey"),
    )
    op.create_index("ix_organizations_role", "organizations", ["role"], unique=False)
    op.create_index("ix_organizations_name", "organizations", ["name"], unique=False)
    op.create_index("ix_organizations_id", "organizations", ["id"], unique=False)
    # ### end Alembic commands ###
