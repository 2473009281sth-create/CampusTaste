from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile
from PIL import Image

from app.core.config import settings
from app.services.images import validate_image
from app.tasks import _thumbnail


def image_bytes(
    *, image_format: str = "PNG", size: tuple[int, int] = (32, 24)
) -> bytes:
    output = BytesIO()
    Image.new("RGB", size, color=(20, 120, 220)).save(output, format=image_format)
    return output.getvalue()


def upload(data: bytes, filename: str = "untrusted-name.bin") -> UploadFile:
    return UploadFile(filename=filename, file=BytesIO(data))


def test_validate_image_uses_decoded_format_not_filename() -> None:
    data = image_bytes(image_format="PNG")

    actual, extension, content_type, width, height = validate_image(
        upload(data, "fake.jpg")
    )

    assert actual == data
    assert (extension, content_type, width, height) == ("png", "image/png", 32, 24)


def test_validate_image_rejects_undecodable_and_oversized_files() -> None:
    with pytest.raises(HTTPException, match="Invalid or undecodable image"):
        validate_image(upload(b"not-an-image"))

    with pytest.raises(HTTPException, match="Image file is too large"):
        validate_image(upload(b"x" * (settings.IMAGE_MAX_BYTES + 1)))


def test_thumbnail_is_bounded_webp_and_repeatable() -> None:
    original = image_bytes(size=(1200, 800))

    first = _thumbnail(original)
    second = _thumbnail(original)

    assert first == second
    with Image.open(BytesIO(first)) as thumbnail:
        assert thumbnail.format == "WEBP"
        assert thumbnail.width <= settings.IMAGE_THUMBNAIL_SIZE
        assert thumbnail.height <= settings.IMAGE_THUMBNAIL_SIZE
