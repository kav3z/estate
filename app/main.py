from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import init_db_and_seed
from app.routers import pages, auth, properties, transactions, dashboards


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db_and_seed()
    yield


app = FastAPI(
    title="Estate — Verified Housing & Land Platform",
    description="Fullstack FastAPI + Jinja2 + SQLModel (SQLite) housing and land platform.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key="estate-super-secret-session-key-2026",
    max_age=60 * 60 * 24 * 7,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(transactions.router)
app.include_router(dashboards.router)

