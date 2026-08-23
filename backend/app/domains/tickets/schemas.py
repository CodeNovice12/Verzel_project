import uuid
from pydantic import BaseModel

from app.domains.tickets.models import TicketStatus


class TicketOut(BaseModel):
    id: uuid.UUID
    reservation_id: uuid.UUID
    qr_signature: str
    status: TicketStatus

    class Config:
        from_attributes = True