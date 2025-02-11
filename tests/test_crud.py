import pytest

from src.crud import create_user, get_merch_item, get_user_by_username
from src.models import MerchItem


@pytest.mark.asyncio
async def test_create_user(db_session):
    user = await create_user(
        db_session,
        "testuser",
        "testpassword",
    )
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_user_by_username(db_session):
    await create_user(
        db_session,
        "testuser",
        "testpassword",
    )
    user = await get_user_by_username(
        db_session,
        "testuser",
    )
    assert user is not None
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_merch_item(db_session):
    item = MerchItem(name="t-shirt", price=100)
    db_session.add(item)
    await db_session.commit()

    found_item = await get_merch_item(db_session, "t-shirt")
    assert found_item is not None
    assert found_item.price == 100
