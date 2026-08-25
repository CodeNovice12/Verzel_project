import uuid
from pydantic import BaseModel, model_validator

from app.domains.reservations.models import ReservationStatus, SeatStatus

from app.domains.reservations.models import ReservationStatus


class ReservationCreate(BaseModel):
    session_id: uuid.UUID
    seat_id: uuid.UUID | None = None
    quantity: int | None = None

    @model_validator(mode="after")
    def check_seat_or_quantity(self):
        if self.seat_id is None and self.quantity is None:
            raise ValueError("Informe seat_id (modo assento) ou quantity (modo pista)")
        if self.seat_id is not None and self.quantity is not None:
            raise ValueError("Informe apenas seat_id OU quantity, não os dois")
        return self


class ReservationOut(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    customer_id: uuid.UUID
    seat_id: uuid.UUID | None
    quantity: int | None
    status: ReservationStatus

    class Config:
        from_attributes = True

class PaymentResult(BaseModel):
    reservation_id: uuid.UUID
    status: ReservationStatus
    message: str
    ticket_id: uuid.UUID | None = None
class SeatOut(BaseModel):
    id: uuid.UUID
    code: str
    status: SeatStatus

    class Config:
        from_attributes = True
