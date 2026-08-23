import uuid
import enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Integer, Numeric, DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SessionMode(str, enum.Enum):
    SEAT_MAP = "seat_map"
    QUANTITY = "quantity"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organizer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    external_ref: Mapped[str | None] = mapped_column(String(50))  # id do TMDb
    category: Mapped[str] = mapped_column(String(50))  # "filme", "show"

    organizer: Mapped["User"] = relationship(back_populates="events")
    sessions: Mapped[list["Session"]] = relationship(back_populates="event", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    venue: Mapped[str] = mapped_column(String(200))
    capacity: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    mode: Mapped[SessionMode] = mapped_column(SqlEnum(SessionMode, name="session_mode"))

    event: Mapped["Event"] = relationship(back_populates="sessions")
    seats: Mapped[list["Seat"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="session")