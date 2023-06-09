"""empty message

Revision ID: 0e5c6fab2864
Revises: f5623f400869
Create Date: 2023-04-11 21:02:10.650115

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0e5c6fab2864"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("login", sa.String(length=20), nullable=False),
        sa.Column("password", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=30), nullable=True),
        sa.Column("first_name", sa.String(length=20), nullable=True),
        sa.Column("last_name", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("login"),
    )
    op.create_table(
        "friendships",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("friend_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["friend_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.UniqueConstraint("user_id", "friend_id", name="unique_friendships"),
    )
    op.create_index(op.f("ix_friendships_user_id"), "friendships", ["user_id"], unique=False)
    op.create_table(
        "login_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_agent", sa.String(length=300), nullable=False),
        sa.Column("auth_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "auth_date"),
        sa.UniqueConstraint("id", "auth_date"),
        postgresql_partition_by="RANGE (auth_date)",
    )
    op.create_table(
        "users_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###
    op.execute(
        """CREATE TABLE IF NOT EXISTS "login_history_2023" PARTITION OF "login_history" FOR VALUES FROM ('2023-1-1 00:00:00') TO ('2024-1-1 00:00:00')"""
    )
    op.execute(
        """CREATE TABLE IF NOT EXISTS "login_history_2024" PARTITION OF "login_history" FOR VALUES FROM ('2024-1-1 00:00:00') TO ('2025-1-1 00:00:00')"""
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users_roles")
    op.drop_table("login_history")
    op.drop_index(op.f("ix_friendships_user_id"), table_name="friendships")
    op.drop_table("friendships")
    op.drop_table("users")
    op.drop_table("roles")
    # ### end Alembic commands ###
