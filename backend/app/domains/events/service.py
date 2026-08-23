import uuid
from fastapi import HTTPException, status

from app.domains.auth.models import User
from app.domains.events.catalog import CatalogProvider, CatalogItem
from app.domains.events.models import Event, Session, SessionMode
from app.domains.events.repository import EventRepository, SessionRepository
from app.domains.events.schemas import EventCreate, SessionCreate
from app.domains.reservations.models import Seat


def generate_seat_codes(capacity: int, seats_per_row: int = 10) -> list[str]:
    codes = []
    row = 0
    col = 1
    while len(codes) < capacity:
        letter = chr(ord("A") + row)
        codes.append(f"{letter}{col}")
        col += 1
        if col > seats_per_row:
            col = 1
            row += 1
    return codes


class EventService:
    def __init__(
        self,
        event_repo: EventRepository,
        session_repo: SessionRepository,
        catalog: CatalogProvider,
    ):
        self.event_repo = event_repo
        self.session_repo = session_repo
        self.catalog = catalog

    async def get_catalog(self) -> list[CatalogItem]:
        return await self.catalog.get_now_playing()

    async def create_event(self, data: EventCreate, organizer: User) -> Event:
        event = Event(
            organizer_id=organizer.id,
            title=data.title,
            external_ref=data.external_ref,
            category=data.category,
        )
        return await self.event_repo.create(event)

    async def list_events(self) -> list[Event]:
        return await self.event_repo.list_all()

    async def get_event(self, event_id: uuid.UUID) -> Event:
        event = await self.event_repo.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        return event

    async def create_session(
        self, event_id: uuid.UUID, data: SessionCreate, organizer: User
    ) -> Session:
        event = await self.get_event(event_id)
        if event.organizer_id != organizer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não é o organizador deste evento",
            )

        session = Session(
            event_id=event.id,
            starts_at=data.starts_at,
            venue=data.venue,
            capacity=data.capacity,
            price=data.price,
            mode=data.mode,
        )
        session = await self.session_repo.create(session)

        if data.mode == SessionMode.SEAT_MAP:
            codes = generate_seat_codes(data.capacity)
            seats = [Seat(session_id=session.id, code=code) for code in codes]
            await self.session_repo.add_seats(seats)

        return session