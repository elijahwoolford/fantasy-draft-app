"""FastAPI app: draft lottery API and (in production) static SPA."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from lottery import HARDCODED_ODDS, run_lottery

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"

app = FastAPI(title="Fantasy Draft Lottery API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DraftRequest(BaseModel):
    teams: list[str] = Field(..., min_length=4, max_length=4)


class DraftResponse(BaseModel):
    draftOrder: list[str]
    odds: list[int]


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/draft", response_model=DraftResponse)
def draft(body: DraftRequest) -> DraftResponse:
    try:
        order = run_lottery(body.teams)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return DraftResponse(draftOrder=order, odds=list(HARDCODED_ODDS))


# Production: serve Vite build from frontend/dist
if FRONTEND_DIST.is_dir():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def spa_index() -> FileResponse:
        return FileResponse(FRONTEND_DIST / "index.html")

    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str) -> FileResponse:
        """Serve files from dist or index.html for SPA routes."""
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
