"""添加图片资源和持久化处理任务

Revision ID: f4d5e6f7a8b9
Revises: e3c4d5e6f7a8
Create Date: 2026-10-03
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "f4d5e6f7a8b9"
down_revision = "e3c4d5e6f7a8"
branch_labels = None
depends_on = None

image_status = postgresql.ENUM(
    "PENDING", "PROCESSING", "READY", "FAILED", name="imagestatus", create_type=False
)
image_job_status = postgresql.ENUM(
    "PENDING",
    "PROCESSING",
    "SUCCEEDED",
    "FAILED",
    name="imagejobstatus",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    image_status.create(bind, checkfirst=True)
    image_job_status.create(bind, checkfirst=True)

    op.create_table(
        "imageasset",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("dish_id", sa.Uuid(), nullable=True),
        sa.Column("review_id", sa.Uuid(), nullable=True),
        sa.Column("original_object_key", sa.String(length=500), nullable=False),
        sa.Column("thumbnail_object_key", sa.String(length=500), nullable=True),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("byte_size", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("status", image_status, nullable=False),
        sa.Column("error_message", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("byte_size > 0", name="ck_image_asset_byte_size_positive"),
        sa.CheckConstraint("width > 0 AND height > 0", name="ck_image_asset_dimensions"),
        sa.CheckConstraint(
            "(dish_id IS NOT NULL AND review_id IS NULL) OR "
            "(dish_id IS NULL AND review_id IS NOT NULL)",
            name="ck_image_asset_one_target",
        ),
        sa.ForeignKeyConstraint(["dish_id"], ["dish.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["review_id"], ["review.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("original_object_key"),
    )
    op.create_index("ix_image_asset_dish_created", "imageasset", ["dish_id", "created_at"])
    op.create_index(
        "ix_image_asset_review_created", "imageasset", ["review_id", "created_at"]
    )
    op.create_index(
        "ix_image_asset_owner_created", "imageasset", ["owner_id", "created_at"]
    )

    op.create_table(
        "imageprocessingjob",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("image_id", sa.Uuid(), nullable=False),
        sa.Column("status", image_job_status, nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("attempts >= 0", name="ck_image_job_attempts_nonnegative"),
        sa.ForeignKeyConstraint(["image_id"], ["imageasset.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("image_id"),
    )
    op.create_index(
        "ix_image_job_dispatch",
        "imageprocessingjob",
        ["status", "next_attempt_at", "created_at"],
    )


def downgrade() -> None:
    op.drop_table("imageprocessingjob")
    op.drop_table("imageasset")
    bind = op.get_bind()
    image_job_status.drop(bind, checkfirst=True)
    image_status.drop(bind, checkfirst=True)
