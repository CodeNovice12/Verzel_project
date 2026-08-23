import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings


def sign_ticket_payload(
    ticket_id: uuid.UUID, reservation_id: uuid.UUID, session_id: uuid.UUID, event_id: uuid.UUID
) -> str:
    payload = {
        "ticket_id": str(ticket_id),
        "reservation_id": str(reservation_id),
        "session_id": str(session_id),
        "event_id": str(event_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=365),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_ticket_payload(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise ValueError("QR inválido, corrompido ou forjado")