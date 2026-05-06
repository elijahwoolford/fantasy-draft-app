# Fantasy Draft Lottery

React + FastAPI app that draws a **4-team** draft order using weighted odds (fixed by slot: **37% / 28% / 20% / 15%** for teams 1–4; enter teams **worst record first**).

The legacy Streamlit version lives in [`archive/`](archive/).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python 3.13)
- Node.js 20+ (for local frontend dev and for Docker builds)

## Local development

**Terminal 1 — backend**

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

**Terminal 2 — frontend**

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The Vite dev server proxies `/api` to the backend on port 8000.

## Backend tests

```bash
cd backend
uv run pytest
```

## Docker (single container)

Builds the frontend, then serves the API + static SPA on port **8000**:

```bash
docker build -t draft-lottery .
docker run --rm -p 8000:8000 draft-lottery
```

Open [http://localhost:8000](http://localhost:8000).

## API

- `GET /api/health` — health check
- `POST /api/draft` — body `{ "teams": ["A","B","C","D"] }` → `{ "draftOrder": [...], "odds": [37,28,20,15] }`
