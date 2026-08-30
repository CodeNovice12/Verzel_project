import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.reservations.models import Seat, Reservation, SeatStatus, ReservationStatus


class SeatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id_for_update(self, seat_id: uuid.UUID) -> Seat | None:
        result = await self.db.execute(
            select(Seat).where(Seat.id == seat_id).with_for_update()
        )
        return result.scalar_one_or_none()

    async def update_status(self, seat: Seat, status: SeatStatus) -> None:
        seat.status = status
        await self.db.commit()

    async def list_by_session(self, session_id: uuid.UUID) -> list[Seat]:
        result = await self.db.execute(
            select(Seat).where(Seat.session_id == session_id).order_by(Seat.code)
        )
        return list(result.scalars().all())


class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_active_by_session(self, session_id: uuid.UUID) -> int:
        """
        Calcula os lugares ocupados somando apenas reservas CONFIRMADAS 
        e PENDENTES (que garantem retenção temporária durante o checkout).
        """
        result = await self.db.execute(
            select(func.coalesce(func.sum(Reservation.quantity), 0)).where(
                Reservation.session_id == session_id,
                Reservation.quantity.isnot(None),
                Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.PENDING]),
            )
        )
        return result.scalar_one()

    async def create(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        await self.db.commit()
        await self.db.refresh(reservation)
        return reservation

    async def get_by_id(self, reservation_id: uuid.UUID) -> Reservation | None:
        result = await self.db.execute(
            select(Reservation).where(Reservation.id == reservation_id)
        )
        return result.scalar_one_or_none()

    async def update_status(self, reservation: Reservation) -> None:
        await self.db.commit()
        await self.db.refresh(reservation)