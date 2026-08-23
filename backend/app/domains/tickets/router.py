from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.auth.dependencies import get_current_user
from app.domains.auth.models import User
from app.domains.tickets.repository import TicketRepository
from app.domains.tickets.schemas import TicketOut
from app.domains.tickets.service import TicketService
from app.domains.reservations.repository import ReservationRepository
from app.domains.events.repository import SessionRepository

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_ticket_service(db: AsyncSession = Depends(get_db)) -> TicketService:
    return TicketService(
        TicketRepository(db),
        ReservationRepository(db),
        SessionRepository(db),
    )


@router.get("/me", response_model=list[TicketOut])
async def my_tickets(
    current_user: User = Depends(get_current_user),
    service: TicketService = Depends(get_ticket_service),
):
    return await service.list_my_tickets(current_user.id)