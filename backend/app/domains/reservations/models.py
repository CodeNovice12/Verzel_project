import uuid
import enum
from sqlalchemy import String, ForeignKey, Integer, Enum as SqlEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SeatStatus(str, enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"


class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        Index("uq_seat_session_code", "session_id", "code", unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"))
    code: Mapped[str] = mapped_column(String(10))  # ex: "A1", "B12"
    status: Mapped[SeatStatus] = mapped_column(
        SqlEnum(SeatStatus, name="seat_status"), default=SeatStatus.AVAILABLE
    )

    session: Mapped["Session"] = relationship(back_populates="seats")
    reservation: Mapped["Reservation | None"] = relationship(back_populates="seat")


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        # Um assento só pode estar vinculado a UMA reserva ativa por vez
        Index("uq_reservation_seat", "seat_id", unique=True, postgresql_where="seat_id IS NOT NULL"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"))
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    seat_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("seats.id"), nullable=True)
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[ReservationStatus] = mapped_column(
        SqlEnum(ReservationStatus, name="reservation_status"), default=ReservationStatus.PENDING
    )

    session: Mapped["Session"] = relationship(back_populates="reservations")
    customer: Mapped["User"] = relationship(back_populates="reservations")
    seat: Mapped["Seat | None"] = relationship(back_populates="reservation")
    ticket: Mapped["Ticket | None"] = relationship(back_populates="reservation", cascade="all, delete-orphan")