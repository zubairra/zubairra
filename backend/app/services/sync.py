from datetime import date, datetime

from sqlalchemy.orm import Session

from app.connectors.kotak import KotakNeoConnector
from app.connectors.zerodha import ZerodhaConnector
from app.models.models import Trade, User
from app.services.financials import calculate_net_pnl, calculate_taxes


def _get_connector(name: str):
    normalized = (name or "").lower()
    if "kotak" in normalized:
        return KotakNeoConnector()
    if "zerodha" in normalized or "kite" in normalized:
        return ZerodhaConnector()
    raise ValueError(f"Unsupported broker: {name}")


async def sync_member_trades(db: Session, user: User) -> int:
    connector = _get_connector(user.broker_name or "")
    raw_trades = await connector.fetch_tradebook(user.access_token or "", user.api_key)

    inserted = 0
    for raw in raw_trades:
        t = connector.normalize_trade(raw, user.broker_name or "unknown")
        turnover = t["quantity"] * t["price"]
        buy_value = turnover if t["side"].upper() == "BUY" else 0.0
        sell_value = turnover if t["side"].upper() == "SELL" else 0.0
        charges = calculate_taxes(t["segment"], turnover)
        net_pnl = calculate_net_pnl(buy_value, sell_value, charges)

        trade = Trade(
            user_id=user.id,
            broker=t["broker"],
            exchange=t["exchange"],
            segment=t["segment"],
            symbol=t["symbol"],
            side=t["side"],
            quantity=t["quantity"],
            price=t["price"],
            buy_value=buy_value,
            sell_value=sell_value,
            brokerage=charges["brokerage"],
            stt=charges["stt"],
            exchange_charges=charges["exchange_charges"],
            gst=charges["gst"],
            net_pnl=net_pnl,
            trade_date=datetime.fromisoformat(str(t["trade_date"])) .date() if isinstance(t["trade_date"], str) else date.today(),
            order_id=t["order_id"],
        )
        db.add(trade)
        inserted += 1

    db.commit()
    return inserted
