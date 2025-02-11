import logging

from decouple import config
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src import auth, crud, database, models, schemas

logging.basicConfig(level=logging.INFO)

DEVELOPMENT: bool = config(
    "DEVELOPMENT",
    default=False,
    cast=bool,
)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/api/auth", response_model=schemas.AuthResponse)
async def authenticate_user(
    auth_data: schemas.AuthRequest,
    db: AsyncSession = Depends(database.get_db),
):
    user = await crud.get_user_by_username(db, auth_data.username)

    if not user:
        user = await crud.create_user(
            db, auth_data.username, auth_data.password
        )
    elif not auth.verify_password(auth_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    token = auth.create_access_token({"sub": user.username})
    return {"token": token}


@app.get("/api/info", response_model=schemas.InfoResponse)
async def get_user_info(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(database.get_db),
):
    username = auth.decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = await crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {
        "coins": user.coins,
        "inventory": [
            {"type": item.type, "quantity": item.quantity}
            for item in user.inventory
        ],
        "coinHistory": {
            "received": [
                {"fromUser": record.from_user, "amount": record.amount}
                for record in user.coin_history
                if record.to_user == username
            ],
            "sent": [
                {"toUser": record.to_user, "amount": record.amount}
                for record in user.coin_history
                if record.from_user == username
            ],
        },
    }


@app.post("/api/sendCoin")
async def send_coin(
    send_data: schemas.SendCoinRequest,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(database.get_db),
):
    username = auth.decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    sender = await crud.get_user_by_username(db, username)
    receiver = await crud.get_user_by_username(db, send_data.toUser)

    if not sender or not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if sender.coins < send_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough coins",
        )

    sender.coins -= send_data.amount
    receiver.coins += send_data.amount

    transaction = models.CoinHistory(
        user_id=sender.id,
        from_user=sender.username,
        to_user=receiver.username,
        amount=send_data.amount,
    )
    db.add(transaction)

    await db.commit()
    await db.refresh(sender)
    await db.refresh(receiver)

    return {"message": "Transaction successful"}


@app.get("/api/buy/{item}")
async def buy_item(
    item: str,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(database.get_db),
):
    username = auth.decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    merch_item = await crud.get_merch_item(db, item)
    if not merch_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    if user.coins < merch_item.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough coins",
        )

    user.coins -= merch_item.price

    inventory_item = next((i for i in user.inventory if i.type == item), None)
    if inventory_item:
        inventory_item.quantity += 1
    else:
        inventory_item = models.InventoryItem(
            type=item, quantity=1, owner_id=user.id
        )
        db.add(inventory_item)

    await db.commit()
    await db.refresh(user)

    return {
        "coins": user.coins,
        "inventory": [
            {"type": i.type, "quantity": i.quantity} for i in user.inventory
        ],
        "coinHistory": {
            "received": [
                {"fromUser": record.from_user, "amount": record.amount}
                for record in user.coin_history
                if record.to_user == username
            ],
            "sent": [
                {"toUser": record.to_user, "amount": record.amount}
                for record in user.coin_history
                if record.from_user == username
            ],
        },
    }


@app.post("/api/reset_coins")
async def reset_coins(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(database.get_db),
):
    if not DEVELOPMENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in DEVELOPMENT mode",
        )

    username = auth.decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.coins = 1000
    await db.commit()
    await db.refresh(user)

    return {"message": f"Balance reset to 1000 for {user.username}"}
