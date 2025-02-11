from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password = Column(String, nullable=False)
    coins = Column(Integer, default=1000)

    inventory = relationship(
        "InventoryItem",
        back_populates="owner",
        lazy="joined",
    )
    coin_history = relationship(
        "CoinHistory",
        back_populates="user",
        lazy="joined",
    )


class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="inventory",
    )


class CoinHistory(Base):
    __tablename__ = "coin_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    from_user = Column(String, nullable=False)
    to_user = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)

    user = relationship(
        "User",
        back_populates="coin_history",
    )


class MerchItem(Base):
    __tablename__ = "merch_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)
