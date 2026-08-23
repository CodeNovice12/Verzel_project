import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.domains.events.models import SessionMode


class EventCreate(BaseModel):
    title: str
    external_ref: str | None = None
    category: str


class EventOut(BaseModel):
    id: uuid.UUID
    organizer_id: uuid.UUID
    title: str
    external_ref: str | None
    category: str

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    starts_at: datetime
    venue: str
    capacity: int
    price: Decimal
    mode: SessionMode


class SessionOut(BaseModel):
    id: uuid.UUID
    event_id: uuid.UUID
    starts_at: datetime
    venue: str
    capacity: int
    price: Decimal
    mode: SessionMode

    class Config:
        from_attributes = True


class EventWithSessionsOut(EventOut):
    sessions: list[SessionOut] = []