import uuid
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import EmailStr
from sqlalchemy import CheckConstraint, DateTime, Index, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class UserRole(StrEnum):
    USER = "user"
    REVIEWER = "reviewer"
    ADMIN = "admin"


class DishStatus(StrEnum):
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"


class ReportReason(StrEnum):
    SPAM = "spam"
    ABUSE = "abuse"
    FALSE_INFORMATION = "false_information"
    OTHER = "other"


class ReportStatus(StrEnum):
    PENDING = "pending"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class ModerationAction(StrEnum):
    REVIEW_HIDDEN = "review_hidden"
    REVIEW_UNHIDDEN = "review_unhidden"
    REPORT_RESOLVED = "report_resolved"
    REPORT_DISMISSED = "report_dismissed"


class ImageStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class ImageJobStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    role: UserRole = Field(default=UserRole.USER, index=True)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    role: UserRole | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list[Item] = Relationship(back_populates="owner", cascade_delete=True)
    submitted_dishes: list[Dish] = Relationship(
        back_populates="submitted_by",
        sa_relationship_kwargs={"foreign_keys": "Dish.submitted_by_id"},
    )
    reviewed_dishes: list[Dish] = Relationship(
        back_populates="reviewed_by",
        sa_relationship_kwargs={"foreign_keys": "Dish.reviewed_by_id"},
    )
    dish_reviews: list[Review] = Relationship(back_populates="user")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


class SchoolBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=32)
    is_active: bool = True


class School(SchoolBase, table=True):
    __table_args__ = (UniqueConstraint("code", name="uq_school_code"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    canteens: list[Canteen] = Relationship(back_populates="school")


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    code: str | None = Field(default=None, min_length=1, max_length=32)
    is_active: bool | None = None


class SchoolPublic(SchoolBase):
    id: uuid.UUID
    created_at: datetime


class SchoolsPublic(SQLModel):
    data: list[SchoolPublic]
    count: int


class CanteenBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    address: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class Canteen(CanteenBase, table=True):
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_canteen_school_name"),
        Index("ix_canteen_school_active", "school_id", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    school_id: uuid.UUID = Field(foreign_key="school.id", nullable=False)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    school: School | None = Relationship(back_populates="canteens")
    stalls: list[Stall] = Relationship(back_populates="canteen")


class CanteenCreate(CanteenBase):
    school_id: uuid.UUID


class CanteenUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    address: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class CanteenPublic(CanteenBase):
    id: uuid.UUID
    school_id: uuid.UUID
    created_at: datetime


class CanteensPublic(SQLModel):
    data: list[CanteenPublic]
    count: int


class StallBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    floor: str | None = Field(default=None, max_length=32)
    location: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class Stall(StallBase, table=True):
    __table_args__ = (
        UniqueConstraint("canteen_id", "name", name="uq_stall_canteen_name"),
        Index("ix_stall_canteen_active", "canteen_id", "is_active"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    canteen_id: uuid.UUID = Field(foreign_key="canteen.id", nullable=False)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    canteen: Canteen | None = Relationship(back_populates="stalls")
    dishes: list[Dish] = Relationship(back_populates="stall")


class StallCreate(StallBase):
    canteen_id: uuid.UUID


class StallUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    floor: str | None = Field(default=None, max_length=32)
    location: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class StallPublic(StallBase):
    id: uuid.UUID
    canteen_id: uuid.UUID
    created_at: datetime


class StallsPublic(SQLModel):
    data: list[StallPublic]
    count: int


class CategoryBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    is_active: bool = True


class Category(CategoryBase, table=True):
    __table_args__ = (UniqueConstraint("name", name="uq_category_name"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    dishes: list[Dish] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    is_active: bool | None = None


class CategoryPublic(CategoryBase):
    id: uuid.UUID
    created_at: datetime


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int


class DishBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal = Field(decimal_places=2, max_digits=10, ge=0)


class Dish(DishBase, table=True):
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_dish_price_nonnegative"),
        Index("ix_dish_stall_status_created", "stall_id", "status", "created_at"),
        Index("ix_dish_submitter_status", "submitted_by_id", "status"),
        CheckConstraint("rating_sum >= 0", name="ck_dish_rating_sum_nonnegative"),
        CheckConstraint("rating_count >= 0", name="ck_dish_rating_count_nonnegative"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    stall_id: uuid.UUID = Field(foreign_key="stall.id", nullable=False)
    category_id: uuid.UUID | None = Field(
        default=None, foreign_key="category.id", ondelete="SET NULL"
    )
    submitted_by_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    status: DishStatus = Field(default=DishStatus.PENDING, index=True)
    review_note: str | None = Field(default=None, max_length=500)
    reviewed_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    reviewed_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    published_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    rating_sum: int = Field(default=0, nullable=False)
    rating_count: int = Field(default=0, nullable=False)
    stall: Stall | None = Relationship(back_populates="dishes")
    category: Category | None = Relationship(back_populates="dishes")
    submitted_by: User | None = Relationship(
        back_populates="submitted_dishes",
        sa_relationship_kwargs={"foreign_keys": "Dish.submitted_by_id"},
    )
    reviewed_by: User | None = Relationship(
        back_populates="reviewed_dishes",
        sa_relationship_kwargs={"foreign_keys": "Dish.reviewed_by_id"},
    )
    reviews: list[Review] = Relationship(back_populates="dish")


class DishCreate(DishBase):
    stall_id: uuid.UUID
    category_id: uuid.UUID | None = None


class DishUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal | None = Field(default=None, decimal_places=2, max_digits=10, ge=0)
    stall_id: uuid.UUID | None = None
    category_id: uuid.UUID | None = None


class DishReview(SQLModel):
    status: DishStatus
    review_note: str | None = Field(default=None, max_length=500)


class DishPublic(DishBase):
    id: uuid.UUID
    stall_id: uuid.UUID
    category_id: uuid.UUID | None
    submitted_by_id: uuid.UUID
    status: DishStatus
    review_note: str | None
    reviewed_by_id: uuid.UUID | None
    reviewed_at: datetime | None
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime
    rating_sum: int
    rating_count: int


class ReviewBase(SQLModel):
    rating: int = Field(ge=1, le=5)
    content: str | None = Field(default=None, max_length=2000)


class Review(ReviewBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "dish_id", name="uq_review_user_dish"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range"),
        CheckConstraint("like_count >= 0", name="ck_review_like_count_nonnegative"),
        Index(
            "ix_review_dish_visible_created",
            "dish_id",
            "is_deleted",
            "is_hidden",
            "created_at",
            "id",
        ),
        Index("ix_review_user_created", "user_id", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    dish_id: uuid.UUID = Field(foreign_key="dish.id", nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    is_hidden: bool = Field(default=False, nullable=False)
    like_count: int = Field(default=0, nullable=False)
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    user: User | None = Relationship(back_populates="dish_reviews")
    dish: Dish | None = Relationship(back_populates="reviews")


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(SQLModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    content: str | None = Field(default=None, max_length=2000)


class ReviewPublic(ReviewBase):
    id: uuid.UUID
    user_id: uuid.UUID
    dish_id: uuid.UUID
    is_deleted: bool
    is_hidden: bool
    like_count: int
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ReviewsPage(SQLModel):
    data: list[ReviewPublic]
    next_cursor: str | None


class ReviewLike(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "review_id", name="uq_review_like_user_review"),
        Index("ix_review_like_review_created", "review_id", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    review_id: uuid.UUID = Field(foreign_key="review.id", nullable=False)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ReviewLikeUpdate(SQLModel):
    liked: bool


class ReviewLikePublic(SQLModel):
    review_id: uuid.UUID
    liked: bool
    like_count: int


class ReviewReport(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "reporter_id", "review_id", name="uq_review_report_reporter_review"
        ),
        Index("ix_review_report_status_created", "status", "created_at", "id"),
        Index("ix_review_report_review_created", "review_id", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    reporter_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    review_id: uuid.UUID = Field(foreign_key="review.id", nullable=False)
    reason: ReportReason
    details: str | None = Field(default=None, max_length=1000)
    status: ReportStatus = Field(default=ReportStatus.PENDING, nullable=False)
    resolution_note: str | None = Field(default=None, max_length=1000)
    handled_by_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    handled_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ReviewReportCreate(SQLModel):
    reason: ReportReason
    details: str | None = Field(default=None, max_length=1000)


class ReviewReportResolve(SQLModel):
    status: ReportStatus
    hide_review: bool = False
    resolution_note: str | None = Field(default=None, max_length=1000)


class ReviewReportPublic(SQLModel):
    id: uuid.UUID
    reporter_id: uuid.UUID
    review_id: uuid.UUID
    reason: ReportReason
    details: str | None
    status: ReportStatus
    resolution_note: str | None
    handled_by_id: uuid.UUID | None
    handled_at: datetime | None
    created_at: datetime


class ReviewReportsPublic(SQLModel):
    data: list[ReviewReportPublic]
    count: int


class ReviewVisibilityUpdate(SQLModel):
    is_hidden: bool
    note: str | None = Field(default=None, max_length=1000)


class ModerationAudit(SQLModel, table=True):
    __table_args__ = (
        Index("ix_moderation_audit_review_created", "review_id", "created_at"),
        Index("ix_moderation_audit_actor_created", "actor_id", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    actor_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    action: ModerationAction
    review_id: uuid.UUID = Field(foreign_key="review.id", nullable=False)
    report_id: uuid.UUID | None = Field(
        default=None, foreign_key="reviewreport.id", ondelete="SET NULL"
    )
    previous_hidden: bool
    new_hidden: bool
    note: str | None = Field(default=None, max_length=1000)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ModerationAuditPublic(SQLModel):
    id: uuid.UUID
    actor_id: uuid.UUID | None
    action: ModerationAction
    review_id: uuid.UUID
    report_id: uuid.UUID | None
    previous_hidden: bool
    new_hidden: bool
    note: str | None
    created_at: datetime


class ModerationAuditsPublic(SQLModel):
    data: list[ModerationAuditPublic]
    count: int


class ImageAsset(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint(
            "(dish_id IS NOT NULL AND review_id IS NULL) OR "
            "(dish_id IS NULL AND review_id IS NOT NULL)",
            name="ck_image_asset_one_target",
        ),
        CheckConstraint("byte_size > 0", name="ck_image_asset_byte_size_positive"),
        CheckConstraint("width > 0 AND height > 0", name="ck_image_asset_dimensions"),
        Index("ix_image_asset_dish_created", "dish_id", "created_at"),
        Index("ix_image_asset_review_created", "review_id", "created_at"),
        Index("ix_image_asset_owner_created", "owner_id", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    dish_id: uuid.UUID | None = Field(default=None, foreign_key="dish.id")
    review_id: uuid.UUID | None = Field(default=None, foreign_key="review.id")
    original_object_key: str = Field(unique=True, max_length=500)
    thumbnail_object_key: str | None = Field(default=None, max_length=500)
    content_type: str = Field(max_length=100)
    byte_size: int
    width: int
    height: int
    status: ImageStatus = Field(default=ImageStatus.PENDING, nullable=False)
    error_message: str | None = Field(default=None, max_length=1000)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ImageProcessingJob(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("attempts >= 0", name="ck_image_job_attempts_nonnegative"),
        Index("ix_image_job_dispatch", "status", "next_attempt_at", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    image_id: uuid.UUID = Field(
        foreign_key="imageasset.id", ondelete="CASCADE", nullable=False, unique=True
    )
    status: ImageJobStatus = Field(default=ImageJobStatus.PENDING, nullable=False)
    attempts: int = Field(default=0, nullable=False)
    next_attempt_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    dispatched_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    finished_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    last_error: str | None = Field(default=None, max_length=1000)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ImageAssetPublic(SQLModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    dish_id: uuid.UUID | None
    review_id: uuid.UUID | None
    content_type: str
    byte_size: int
    width: int
    height: int
    status: ImageStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class ImageAccessPublic(SQLModel):
    url: str
    expires_in: int


class ImageAssetsPublic(SQLModel):
    data: list[ImageAssetPublic]
    count: int


class RankingEntry(SQLModel):
    dish: DishPublic
    average_rating: Decimal
    rating_count: int
    weighted_score: Decimal


class RankingsPublic(SQLModel):
    data: list[RankingEntry]
    scope_average: Decimal
    prior_weight: int
    generated_at: datetime


class DishesPublic(SQLModel):
    data: list[DishPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
    type: str | None = None
    jti: str | None = None
    family: str | None = None


class RefreshTokenRequest(SQLModel):
    refresh_token: str


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
