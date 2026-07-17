from pathlib import Path
import os
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.routers import metrics, contracts, properties

# Path prefix no App Space Hub (auth-proxy encaminha /{slug}/...).
# Local/tests: vazio. Deploy hub: ROOT_PATH=/{slug}
ROOT_PATH = os.environ.get("ROOT_PATH", "").rstrip("/")


class StripRootPathMiddleware(BaseHTTPMiddleware):
    """Remove hub path_prefix so routers keep /health and /api/v1/*."""

    async def dispatch(self, request: Request, call_next):
        if ROOT_PATH and request.scope["path"].startswith(ROOT_PATH):
            path = request.scope["path"][len(ROOT_PATH) :] or "/"
            request.scope["path"] = path
        return await call_next(request)


app = FastAPI(title="real estate control", root_path=ROOT_PATH or "")
if ROOT_PATH:
    app.add_middleware(StripRootPathMiddleware)

# CORS middleware (AC-2.6)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP: permitir todas as origens (ajustar em produção)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """
    Health check endpoint
    AC-2.5: Retorna status do backend com timestamp
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# API routes
app.include_router(metrics.router)
app.include_router(contracts.router)
app.include_router(properties.router)

_dist = Path("dist")
if _dist.is_dir():
    from fastapi.staticfiles import StaticFiles

    # AS1I: SPA na raiz (CAS return_to + OpenAPI GET /)
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="frontend")
else:

    @app.get("/")
    def root():
        return {"message": "Hello from real estate control"}
