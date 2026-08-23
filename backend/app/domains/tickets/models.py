import uuid
import enum
from sqlalchemy import String, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TicketStatus(str, enum.Enum):
    VALID = "valid"
    USED = "used"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    reservation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reservations.id"), unique=True)
    qr_signature: Mapped[str] = mapped_column(String(512))  # payload assinado (HMAC/JWT)
    status: Mapped[TicketStatus] = mapped_column(
        SqlEnum(TicketStatus, name="ticket_status"), default=TicketStatus.VALID
    )

    reservation: Mapped["Reservation"] = relationship(back_populates="ticket")