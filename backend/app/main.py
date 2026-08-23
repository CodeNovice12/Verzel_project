from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.database import engine
from app.core import models_registry  # noqa
from app.domains.auth.router import router as auth_router
from app.domains.events.router import router as events_router
from app.domains.reservations.router import router as reservations_router
from app.domains.tickets.router import router as tickets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    print("✅ Conexão com o banco validada")
    yield


app = FastAPI(title="Verzel Project API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(events_router)
app.include_router(reservations_router)
app.include_router(tickets_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}