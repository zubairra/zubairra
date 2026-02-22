from datetime import date

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "member"


class UserTokenUpdate(BaseModel):
    broker_name: str
    access_token: str
    api_key: str | None = None


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    broker_name: str | None

    class Config:
        from_attributes = True


class TradeOut(BaseModel):
    symbol: str
    segment: str
    side: str
    quantity: int
    price: float
    net_pnl: float
    trade_date: date

    class Config:
        from_attributes = True


class MonthlyPnL(BaseModel):
    month: str
    pnl: float


class SyncRequest(BaseModel):
    member_id: int
