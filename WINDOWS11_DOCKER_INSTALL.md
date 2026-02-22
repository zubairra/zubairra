# Windows 11 Installation Guide (Docker Desktop UI + GitHub Image Pull)

This guide is written for **basic users** to run the app on Windows 11 using Docker Desktop.

---

## 1) Prerequisites (one-time)

1. Install **Docker Desktop for Windows**:
   - Download from: https://www.docker.com/products/docker-desktop/
   - During installation, enable **WSL2** when prompted.
2. Restart your computer if Docker asks.
3. Open Docker Desktop and confirm it says **Engine running**.
4. Install **Git for Windows** (if not installed): https://git-scm.com/download/win

---

## 2) Option A — Run directly from source code (recommended for testing)

### Step A1: Download project from GitHub

- Open PowerShell and run:

```powershell
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_REPO_FOLDER>
```

### Step A2: Start with Docker Compose

```powershell
docker compose up --build -d
```

This starts:
- Backend API: `http://localhost:8000`
- Frontend UI: `http://localhost:5173`

### Step A3: Verify services in Docker Desktop UI

1. Open Docker Desktop.
2. Go to **Containers**.
3. You should see the project stack with two containers:
   - `backend`
   - `frontend`
4. Status must be **Running**.

### Step A4: Open app in browser

- Frontend dashboard: `http://localhost:5173`
- API health check: `http://localhost:8000/health`

Expected health response:

```json
{"status":"ok"}
```

### Step A5: Stop / Restart later

- Stop:

```powershell
docker compose down
```

- Start again:

```powershell
docker compose up -d
```

---

## 3) Option B — Pull prebuilt images from GitHub Container Registry (GHCR)

Use this when images are published by the repo owner.

## Step B1: Login to GHCR

1. Create a GitHub **Personal Access Token** with `read:packages` permission.
2. In PowerShell:

```powershell
echo <YOUR_GITHUB_PAT> | docker login ghcr.io -u <YOUR_GITHUB_USERNAME> --password-stdin
```

## Step B2: Pull images

> Replace image names with your actual published image paths.

```powershell
docker pull ghcr.io/<owner>/<repo>-backend:latest
docker pull ghcr.io/<owner>/<repo>-frontend:latest
```

## Step B3: Run containers manually

```powershell
docker network create trading-net

docker volume create trading-db

docker run -d --name trading-backend --network trading-net -p 8000:8000 \
  -e DATABASE_URL=sqlite:////data/trading_journal.db \
  -v trading-db:/data \
  ghcr.io/<owner>/<repo>-backend:latest

docker run -d --name trading-frontend --network trading-net -p 5173:5173 \
  -e VITE_API_BASE_URL=http://localhost:8000/api \
  ghcr.io/<owner>/<repo>-frontend:latest
```

Now open `http://localhost:5173`.

---

## 4) Configure for your 50 members

1. Create users through API (`POST /api/users`) or your admin workflow.
2. Each morning, member enters:
   - Broker name (Kotak / Zerodha)
   - Session token (or TOTP-generated session token)
   - Zerodha API key (member-specific)
3. Click **Daily Sync** per member.
4. Use toggle for:
   - **Aggregated Firm P&L**
   - **Individual Member P&L**

---

## 5) Troubleshooting (Windows 11)

### Issue: Port already in use
- If `5173` or `8000` is busy, close conflicting apps or edit `docker-compose.yml` ports.

### Issue: Docker engine not running
- Open Docker Desktop and wait until status shows **Running**.

### Issue: Cannot pull GHCR image
- Re-check PAT permission (`read:packages`) and image path spelling.

### Issue: UI loads but no data
- Confirm backend health URL works: `http://localhost:8000/health`.
- Confirm frontend env points to backend API: `VITE_API_BASE_URL=http://localhost:8000/api`.

---

## 6) Recommended simple release flow for admin

1. Push code to GitHub.
2. Build and publish backend/frontend images to GHCR using GitHub Actions.
3. Share only these 3 commands with users:
   - `docker login ghcr.io ...`
   - `docker pull ...backend...`
   - `docker pull ...frontend...`
4. Users run containers from Docker Desktop UI or provided commands.

