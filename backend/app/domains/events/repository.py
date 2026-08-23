import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.events.models import Event, Session
from app.domains.reservations.models import Seat


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event: Event) -> Event:
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_by_id(self, event_id: uuid.UUID) -> Event | None:
        result = await self.db.execute(
            select(Event).options(selectinload(Event.sessions)).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Event]:
        result = await self.db.execute(
            select(Event).options(selectinload(Event.sessions))
        )
        return list(result.scalars().all())


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, session_id: uuid.UUID) -> Session | None:
        result = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def create(self, session: Session) -> Session:
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def add_seats(self, seats: list[Seat]) -> None:
        self.db.add_all(seats)
        await self.db.commit()