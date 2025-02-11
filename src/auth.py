from datetime import datetime, timedelta

from decouple import config
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = config(
    "SECRET_KEY",
    default="abcde1234",
    cast=str,
)
ALGORITHM = config(
    "ALGORITHM",
    default="HS256",
    cast=str,
)
ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    default=15,
    cast=int,
)

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return password_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()

    expire: datetime = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
