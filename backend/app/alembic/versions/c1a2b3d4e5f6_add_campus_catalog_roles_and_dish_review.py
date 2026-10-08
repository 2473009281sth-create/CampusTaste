"""添加校园层级、用户角色和菜品审核

Revision ID: c1a2b3d4e5f6
Revises: fe56fa70289e
Create Date: 2026-09-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "c1a2b3d4e5f6"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None

user_role = postgresql.ENUM(
    "USER", "REVIEWER", "ADMIN", name="userrole", create_type=False
)
dish_status = postgresql.ENUM(
    "PENDING", "PUBLISHED", "REJECTED", name="dishstatus", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    dish_status.create(bind, checkfirst=True)

    op.add_column(
        "user",
        sa.Column("role", user_role, nullable=False, server_default="USER"),
    )
    op.create_index(op.f("ix_user_role"), "user", ["role"], unique=False)
    op.execute('UPDATE "user" SET role = \'ADMIN\' WHERE is_superuser = true')
    op.alter_column("user", "role", server_default=None)

    op.create_table(
        "school",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_school_code"),
    )
    op.create_table(
        "category",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_category_name"),
    )
    op.create_table(
        "canteen",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("school_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["school_id"], ["school.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("school_id", "name", name="uq_canteen_school_name"),
    )
    op.create_index(
        "ix_canteen_school_active", "canteen", ["school_id", "is_active"]
    )
    op.create_table(
        "stall",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("floor", sa.String(length=32), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("canteen_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["canteen_id"], ["canteen.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("canteen_id", "name", name="uq_stall_canteen_name"),
    )
    op.create_index(
        "ix_stall_canteen_active", "stall", ["canteen_id", "is_active"]
    )
    op.create_table(
        "dish",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("stall_id", sa.Uuid(), nullable=False),
        sa.Column("category_id", sa.Uuid(), nullable=True),
        sa.Column("submitted_by_id", sa.Uuid(), nullable=False),
        sa.Column("status", dish_status, nullable=False),
        sa.Column("review_note", sa.String(length=500), nullable=True),
        sa.Column("reviewed_by_id", sa.Uuid(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("price >= 0", name="ck_dish_price_nonnegative"),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["reviewed_by_id"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["stall_id"], ["stall.id"]),
        sa.ForeignKeyConstraint(["submitted_by_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dish_status"), "dish", ["status"], unique=False)
    op.create_index(
        "ix_dish_stall_status_created",
        "dish",
        ["stall_id", "status", "created_at"],
    )
    op.create_index(
        "ix_dish_submitter_status", "dish", ["submitted_by_id", "status"]
    )


def downgrade() -> None:
    op.drop_table("dish")
    op.drop_table("stall")
    op.drop_table("canteen")
    op.drop_table("category")
    op.drop_table("school")
    op.drop_index(op.f("ix_user_role"), table_name="user")
    op.drop_column("user", "role")
    bind = op.get_bind()
    dish_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
