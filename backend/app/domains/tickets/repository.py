import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.tickets.models import Ticket
from app.domains.reservations.models import Reservation


class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket

    async def persist(self, ticket: Ticket) -> Ticket:
        # usado depois de mudar um atributo (assinatura, status) num ticket já existente
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket

    async def get_by_id(self, ticket_id: uuid.UUID) -> Ticket | None:
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one_or_none()

    async def get_by_reservation_id(self, reservation_id: uuid.UUID) -> Ticket | None:
        result = await self.db.execute(
            select(Ticket).where(Ticket.reservation_id == reservation_id)
        )
        return result.scalar_one_or_none()

    async def list_by_customer(self, customer_id: uuid.UUID) -> list[Ticket]:
        result = await self.db.execute(
            select(Ticket)
            .join(Reservation, Ticket.reservation_id == Reservation.id)
            .where(Reservation.customer_id == customer_id)
        )
        return list(result.scalars().all())