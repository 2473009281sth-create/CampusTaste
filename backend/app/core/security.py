import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from app.core.config import settings

password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(UTC) + expires_delta
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "jti": str(uuid.uuid4()),
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: str | Any, *, family: str | None = None
) -> tuple[str, str, str, int]:
    now = datetime.now(UTC)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    family_id = family or str(uuid.uuid4())
    token = jwt.encode(
        {
            "exp": expire,
            "iat": now,
            "sub": str(subject),
            "type": "refresh",
            "jti": jti,
            "family": family_id,
        },
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return token, jti, family_id, int((expire - now).total_seconds())


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def verify_password(
    plain_password: str, hashed_password: str
) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)
