import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep, get_current_reviewer
from app.models import (
    ImageAccessPublic,
    ImageAsset,
    ImageAssetPublic,
    ImageAssetsPublic,
    ImageStatus,
    User,
)
from app.services.images import (
    can_access_image,
    create_dish_image,
    create_review_image,
    get_image_url,
    retry_image,
)

router = APIRouter(tags=["images"])


def _get_image(session: SessionDep, image_id: uuid.UUID) -> ImageAsset:
    image = session.get(ImageAsset, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.post("/dishes/{dish_id}/images", response_model=ImageAssetPublic)
def upload_dish_image(
    session: SessionDep,
    current_user: CurrentUser,
    dish_id: uuid.UUID,
    file: Annotated[UploadFile, File()],
) -> Any:
    return create_dish_image(
        session=session, dish_id=dish_id, file=file, user=current_user
    )


@router.post("/reviews/{review_id}/images", response_model=ImageAssetPublic)
def upload_review_image(
    session: SessionDep,
    current_user: CurrentUser,
    review_id: uuid.UUID,
    file: Annotated[UploadFile, File()],
) -> Any:
    return create_review_image(
        session=session, review_id=review_id, file=file, user=current_user
    )


@router.get("/image-jobs/failed", response_model=ImageAssetsPublic)
def read_failed_images(
    session: SessionDep,
    reviewer: Annotated[User, Depends(get_current_reviewer)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    del reviewer
    condition = ImageAsset.status == ImageStatus.FAILED
    images = session.exec(
        select(ImageAsset)
        .where(condition)
        .order_by(col(ImageAsset.updated_at).desc())
        .offset(skip)
        .limit(limit)
    ).all()
    count = session.exec(
        select(func.count()).select_from(ImageAsset).where(condition)
    ).one()
    return ImageAssetsPublic(data=images, count=count)


@router.get("/images/{image_id}", response_model=ImageAssetPublic)
def read_image(
    session: SessionDep, current_user: CurrentUser, image_id: uuid.UUID
) -> Any:
    image = _get_image(session, image_id)
    if not can_access_image(session, image, current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return image


@router.get("/images/{image_id}/original-url", response_model=ImageAccessPublic)
def read_original_url(
    session: SessionDep, current_user: CurrentUser, image_id: uuid.UUID
) -> Any:
    return get_image_url(
        session=session,
        image=_get_image(session, image_id),
        user=current_user,
        thumbnail=False,
    )


@router.get("/images/{image_id}/thumbnail-url", response_model=ImageAccessPublic)
def read_thumbnail_url(
    session: SessionDep, current_user: CurrentUser, image_id: uuid.UUID
) -> Any:
    return get_image_url(
        session=session,
        image=_get_image(session, image_id),
        user=current_user,
        thumbnail=True,
    )


@router.post("/images/{image_id}/retry", response_model=ImageAssetPublic)
def retry_failed_image(
    session: SessionDep, current_user: CurrentUser, image_id: uuid.UUID
) -> Any:
    return retry_image(
        session=session,
        image=_get_image(session, image_id),
        user=current_user,
    )
