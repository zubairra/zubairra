## Multi-Broker Trading Journal & Financial Dashboard

Full-stack project for up to 50 members using FastAPI, React, Tailwind, Recharts, and SQLite.

### Features
- Member registration and broker token management (daily token/session input).
- Admin toggle for **Aggregated Firm P&L** vs **Individual Member P&L**.
- Daily sync endpoint per member.
- Broker connector abstraction for Kotak Neo + Zerodha with easy extension for Upstox/Dhan.
- Net P&L calculation with brokerage + STT + exchange charges + GST.
- Daily performance table + monthly P&L chart UI.

### SQL schema
- See `SQL_SCHEMA.sql`.

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker (Windows 11 Docker Desktop friendly)
```bash
docker compose up --build
```

### API Notes (cost control)
- Zerodha should use per-member API key/token to avoid rate-limit concentration.
- Kotak tokens can be refreshed by scheduled automation (e.g., 9:15 AM task).
- Charges are modeled in `calculate_taxes` and can be revised as exchange rates change.

### Good-to-have recommendations
- Add Celery/APS cheduler job for unattended morning token validation + sync queues.
- Add Redis caching and request throttling if 50 concurrent syncs start together.
- Optional integrations later: Upstox + Dhan via `BrokerConnector` subclasses.

## Windows 11 Quick Install (Docker Desktop UI)
For step-by-step beginner instructions (including GitHub image pull via GHCR), see:
- `WINDOWS11_DOCKER_INSTALL.md`

