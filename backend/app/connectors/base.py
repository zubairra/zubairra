from abc import ABC, abstractmethod
from datetime import date


class BrokerConnector(ABC):
    @abstractmethod
    async def fetch_tradebook(self, access_token: str, api_key: str | None = None) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_positions(self, access_token: str, api_key: str | None = None) -> list[dict]:
        raise NotImplementedError

    @staticmethod
    def normalize_trade(raw: dict, broker: str) -> dict:
        return {
            "broker": broker,
            "exchange": raw.get("exchange", "NSE"),
            "segment": raw.get("segment", "EQ"),
            "symbol": raw.get("symbol") or raw.get("tradingsymbol", "UNKNOWN"),
            "side": raw.get("side") or raw.get("transaction_type", "BUY"),
            "quantity": int(raw.get("quantity", 0)),
            "price": float(raw.get("price", raw.get("average_price", 0))),
            "trade_date": raw.get("trade_date", str(date.today())),
            "order_id": str(raw.get("order_id", raw.get("orderid", ""))),
        }
