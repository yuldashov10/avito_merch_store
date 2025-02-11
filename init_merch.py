import asyncio

from sqlalchemy.sql import text

from src.database import SessionLocal
from src.models import MerchItem

MERCH_ITEMS: dict[str, int] = {
    "t-shirt": 80,
    "cup": 20,
    "book": 50,
    "pen": 10,
    "powerbank": 200,
    "hoody": 300,
    "umbrella": 200,
    "socks": 10,
    "wallet": 50,
    "pink-hoody": 500,
}


async def init_merch() -> None:
    async with SessionLocal() as db:
        existing_items: set[str] = {
            item.name
            for item in (
                await db.execute(text("SELECT name FROM merch_items"))
            ).scalars()
        }

        for name, price in MERCH_ITEMS.items():
            if name not in existing_items:
                db.add(MerchItem(name=name, price=price))

        await db.commit()


if __name__ == "__main__":
    asyncio.run(init_merch())
