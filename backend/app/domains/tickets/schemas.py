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

class TicketValidationRequest(BaseModel):
    code: str  # o qr_signature completo, vindo da câmera ou digitado manualmente
    session_id: uuid.UUID  # a sessão que a portaria está validando (contexto do evento na entrada)


class TicketValidationResult(BaseModel):
    result: str  # "valid" | "invalid" | "already_used" | "wrong_event"
    message: str