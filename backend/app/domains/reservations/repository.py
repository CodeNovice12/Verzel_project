import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.reservations.models import Seat, Reservation, SeatStatus


class SeatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id_for_update(self, seat_id: uuid.UUID) -> Seat | None:
        # with_for_update: trava a linha no banco até o fim da transação —
        # ninguém mais consegue ler/alterar esse assento até essa transação terminar
        result = await self.db.execute(
            select(Seat).where(Seat.id == seat_id).with_for_update()
        )
        return result.scalar_one_or_none()

    async def update_status(self, seat: Seat, status: SeatStatus) -> None:
        seat.status = status
        await self.db.commit()


class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_confirmed_by_session(self, session_id: uuid.UUID) -> int:
        from sqlalchemy import func

        result = await self.db.execute(
            select(func.coalesce(func.sum(Reservation.quantity), 0)).where(
                Reservation.session_id == session_id,
                Reservation.quantity.isnot(None),
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