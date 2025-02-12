from src.auth import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


def test_jwt_token():
    token = create_access_token({"sub": "testuser"})
    decoded_username = decode_access_token(token)
    assert decoded_username == "testuser"


def test_invalid_token():
    assert decode_access_token("invalid_token") is None
