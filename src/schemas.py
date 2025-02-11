from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


class InfoResponse(BaseModel):
    coins: int
    inventory: list
    coinHistory: dict


class SendCoinRequest(BaseModel):
    toUser: str
    amount: int
