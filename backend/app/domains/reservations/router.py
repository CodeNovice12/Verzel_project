import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.auth.dependencies import require_role
from app.domains.auth.models import User, UserRole
from app.domains.events.repository import SessionRepository
from app.domains.reservations.repository import SeatRepository, ReservationRepository
from app.domains.reservations.schemas import ReservationCreate, ReservationOut
from app.domains.reservations.service import ReservationService

router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_service(db: AsyncSession = Depends(get_db)) -> ReservationService:
    return ReservationService(
        SeatRepository(db),
        ReservationRepository(db),
        SessionRepository(db),
    )


@router.post("", response_model=ReservationOut, status_code=201)
async def create_reservation(
    data: ReservationCreate,
    current_user: User = Depends(require_role(UserRole.CUSTOMER)),
    service: ReservationService = Depends(get_reservation_service),
):
    return await service.create_reservation(data, current_user)