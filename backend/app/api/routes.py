from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Trade, User
from app.schemas.schemas import SyncRequest, TradeOut, UserCreate, UserOut, UserTokenUpdate
from app.services.auth import hash_password
from app.services.sync import sync_member_trades

router = APIRouter()


@router.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/token", response_model=UserOut)
def update_broker_token(user_id: int, payload: UserTokenUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.broker_name = payload.broker_name
    user.access_token = payload.access_token
    user.api_key = payload.api_key
    user.token_updated_at = func.now()
    db.commit()
    db.refresh(user)
    return user


@router.post("/sync/daily")
async def daily_sync(payload: SyncRequest, db: Session = Depends(get_db)):
    user = db.get(User, payload.member_id)
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    if not user.access_token or not user.broker_name:
        raise HTTPException(status_code=400, detail="Token/broker missing")
    inserted = await sync_member_trades(db, user)
    return {"status": "ok", "inserted": inserted}


@router.get("/performance/daily", response_model=list[TradeOut])
def daily_performance(member_id: int, query_date: date | None = None, db: Session = Depends(get_db)):
    query_date = query_date or date.today()
    return (
        db.query(Trade)
        .filter(Trade.user_id == member_id, Trade.trade_date == query_date)
        .order_by(Trade.created_at.desc())
        .all()
    )


@router.get("/performance/monthly")
def monthly_pnl(member_id: int | None = None, aggregate: bool = False, db: Session = Depends(get_db)):
    q = db.query(func.strftime("%Y-%m", Trade.trade_date).label("month"), func.sum(Trade.net_pnl).label("pnl"))
    if not aggregate and member_id is not None:
        q = q.filter(Trade.user_id == member_id)
    rows = q.group_by("month").order_by("month").all()
    return [{"month": r.month, "pnl": round(r.pnl or 0, 2)} for r in rows]
