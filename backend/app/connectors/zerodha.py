import httpx

from app.connectors.base import BrokerConnector


class ZerodhaConnector(BrokerConnector):
    base_url = "https://api.kite.trade"

    async def fetch_tradebook(self, access_token: str, api_key: str | None = None) -> list[dict]:
        if not api_key:
            raise ValueError("Zerodha requires member-specific API key")
        headers = {"Authorization": f"token {api_key}:{access_token}"}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(f"{self.base_url}/trades", headers=headers)
            resp.raise_for_status()
            payload = resp.json()
        return payload.get("data", [])

    async def fetch_positions(self, access_token: str, api_key: str | None = None) -> list[dict]:
        if not api_key:
            raise ValueError("Zerodha requires member-specific API key")
        headers = {"Authorization": f"token {api_key}:{access_token}"}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(f"{self.base_url}/portfolio/positions", headers=headers)
            resp.raise_for_status()
            payload = resp.json()
        return payload.get("data", {}).get("net", [])
