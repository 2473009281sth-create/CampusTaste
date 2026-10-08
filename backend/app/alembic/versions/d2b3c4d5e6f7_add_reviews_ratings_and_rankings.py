"""添加评价和菜品评分聚合

Revision ID: d2b3c4d5e6f7
Revises: c1a2b3d4e5f6
Create Date: 2026-09-26
"""

import sqlalchemy as sa
from alembic import op

revision = "d2b3c4d5e6f7"
down_revision = "c1a2b3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "dish", sa.Column("rating_sum", sa.Integer(), server_default="0", nullable=False)
    )
    op.add_column(
        "dish",
        sa.Column("rating_count", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_check_constraint(
        "ck_dish_rating_sum_nonnegative", "dish", "rating_sum >= 0"
    )
    op.create_check_constraint(
        "ck_dish_rating_count_nonnegative", "dish", "rating_count >= 0"
    )
    op.alter_column("dish", "rating_sum", server_default=None)
    op.alter_column("dish", "rating_count", server_default=None)

    op.create_table(
        "review",
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=2000), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("dish_id", sa.Uuid(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range"),
        sa.ForeignKeyConstraint(["dish_id"], ["dish.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "dish_id", name="uq_review_user_dish"),
    )
    op.create_index(
        "ix_review_dish_visible_created",
        "review",
        ["dish_id", "is_deleted", "is_hidden", "created_at", "id"],
    )
    op.create_index(
        "ix_review_user_created", "review", ["user_id", "created_at"]
    )


def downgrade() -> None:
    op.drop_table("review")
    op.drop_constraint("ck_dish_rating_count_nonnegative", "dish", type_="check")
    op.drop_constraint("ck_dish_rating_sum_nonnegative", "dish", type_="check")
    op.drop_column("dish", "rating_count")
    op.drop_column("dish", "rating_sum")
