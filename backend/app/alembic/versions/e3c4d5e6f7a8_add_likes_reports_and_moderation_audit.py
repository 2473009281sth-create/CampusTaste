"""添加点赞、举报和内容治理审计

Revision ID: e3c4d5e6f7a8
Revises: d2b3c4d5e6f7
Create Date: 2026-10-01
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "e3c4d5e6f7a8"
down_revision = "d2b3c4d5e6f7"
branch_labels = None
depends_on = None

report_reason = postgresql.ENUM(
    "SPAM", "ABUSE", "FALSE_INFORMATION", "OTHER", name="reportreason", create_type=False
)
report_status = postgresql.ENUM(
    "PENDING", "RESOLVED", "DISMISSED", name="reportstatus", create_type=False
)
moderation_action = postgresql.ENUM(
    "REVIEW_HIDDEN",
    "REVIEW_UNHIDDEN",
    "REPORT_RESOLVED",
    "REPORT_DISMISSED",
    name="moderationaction",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    report_reason.create(bind, checkfirst=True)
    report_status.create(bind, checkfirst=True)
    moderation_action.create(bind, checkfirst=True)

    op.add_column(
        "review",
        sa.Column("like_count", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_check_constraint(
        "ck_review_like_count_nonnegative", "review", "like_count >= 0"
    )
    op.alter_column("review", "like_count", server_default=None)

    op.create_table(
        "reviewlike",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("review_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["review_id"], ["review.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "review_id", name="uq_review_like_user_review"
        ),
    )
    op.create_index(
        "ix_review_like_review_created",
        "reviewlike",
        ["review_id", "created_at"],
    )

    op.create_table(
        "reviewreport",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("reporter_id", sa.Uuid(), nullable=False),
        sa.Column("review_id", sa.Uuid(), nullable=False),
        sa.Column("reason", report_reason, nullable=False),
        sa.Column("details", sa.String(length=1000), nullable=True),
        sa.Column("status", report_status, nullable=False),
        sa.Column("resolution_note", sa.String(length=1000), nullable=True),
        sa.Column("handled_by_id", sa.Uuid(), nullable=True),
        sa.Column("handled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["handled_by_id"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["reporter_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["review_id"], ["review.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "reporter_id", "review_id", name="uq_review_report_reporter_review"
        ),
    )
    op.create_index(
        "ix_review_report_status_created",
        "reviewreport",
        ["status", "created_at", "id"],
    )
    op.create_index(
        "ix_review_report_review_created",
        "reviewreport",
        ["review_id", "created_at"],
    )

    op.create_table(
        "moderationaudit",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("action", moderation_action, nullable=False),
        sa.Column("review_id", sa.Uuid(), nullable=False),
        sa.Column("report_id", sa.Uuid(), nullable=True),
        sa.Column("previous_hidden", sa.Boolean(), nullable=False),
        sa.Column("new_hidden", sa.Boolean(), nullable=False),
        sa.Column("note", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["actor_id"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["report_id"], ["reviewreport.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["review_id"], ["review.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_moderation_audit_review_created",
        "moderationaudit",
        ["review_id", "created_at"],
    )
    op.create_index(
        "ix_moderation_audit_actor_created",
        "moderationaudit",
        ["actor_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_table("moderationaudit")
    op.drop_table("reviewreport")
    op.drop_table("reviewlike")
    op.drop_constraint("ck_review_like_count_nonnegative", "review", type_="check")
    op.drop_column("review", "like_count")

    bind = op.get_bind()
    moderation_action.drop(bind, checkfirst=True)
    report_status.drop(bind, checkfirst=True)
    report_reason.drop(bind, checkfirst=True)
