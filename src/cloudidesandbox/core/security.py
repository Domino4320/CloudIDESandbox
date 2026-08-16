from datetime import datetime, timedelta, timezone
from typing import Literal
from src.cloudidesandbox.core.config import security_config
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, PyJWTError
from src.cloudidesandbox.exceptions.security import (
    InvalidTokenError as CustomInvalidTokenError,
    TokenExpiredError,
    TokenError,
)
import uuid

password_hash = PasswordHash((Argon2Hasher(),))
DUMMY_HASH = password_hash.hash("dummy_password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_jwt(
    subject: str,
    expires_delta: timedelta,
    token_type: Literal["access", "refresh"],
    extras: dict | None = None,
) -> dict:
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())
    payload = {
        "sub": subject,
        "exp": now + expires_delta,
        "iat": now,
        "type": token_type,
        "jti": jti,
    }
    if extras:
        payload.update(extras)
    encoded_jwt = jwt.encode(
        payload,
        security_config.SECRET_KEY,
        security_config.ALGORITHM,
    )
    return encoded_jwt, jti


def get_payload(jwt_token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt_token, security_config.SECRET_KEY, (security_config.ALGORITHM,)
        )
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except InvalidTokenError:
        raise CustomInvalidTokenError()
    except PyJWTError:
        raise TokenError()
    return payload
