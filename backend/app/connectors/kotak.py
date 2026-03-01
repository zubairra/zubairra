import httpx

from app.connectors.base import BrokerConnector


class KotakNeoConnector(BrokerConnector):
    base_url = "https://napi.kotaksecurities.com"

    async def fetch_tradebook(self, access_token: str, api_key: str | None = None) -> list[dict]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(f"{self.base_url}/tradebook", headers=headers)
            resp.raise_for_status()
            payload = resp.json()
        return payload.get("data", payload if isinstance(payload, list) else [])

    async def fetch_positions(self, access_token: str, api_key: str | None = None) -> list[dict]:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(f"{self.base_url}/positions", headers=headers)
            resp.raise_for_status()
            payload = resp.json()
        return payload.get("data", payload if isinstance(payload, list) else [])
