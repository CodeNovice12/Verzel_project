import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.auth.dependencies import get_current_user, require_role
from app.domains.auth.models import User, UserRole
from app.domains.events.catalog import CatalogProvider, MockCatalogProvider
from app.domains.events.repository import EventRepository, SessionRepository
from app.domains.events.schemas import (
    EventCreate, EventOut, EventWithSessionsOut, SessionCreate, SessionOut
)
from app.domains.events.service import EventService

router = APIRouter(prefix="/events", tags=["events"])


def get_catalog_provider() -> CatalogProvider:
    return MockCatalogProvider()


def get_event_service(
    db: AsyncSession = Depends(get_db),
    catalog: CatalogProvider = Depends(get_catalog_provider),
) -> EventService:
    return EventService(EventRepository(db), SessionRepository(db), catalog)


@router.get("/catalog")
async def get_catalog(service: EventService = Depends(get_event_service)):
    return await service.get_catalog()


@router.post("", response_model=EventOut, status_code=201)
async def create_event(
    data: EventCreate,
    current_user: User = Depends(require_role(UserRole.ORGANIZER)),
    service: EventService = Depends(get_event_service),
):
    return await service.create_event(data, current_user)


@router.get("", response_model=list[EventWithSessionsOut])
async def list_events(service: EventService = Depends(get_event_service)):
    return await service.list_events()


@router.get("/{event_id}", response_model=EventWithSessionsOut)
async def get_event(event_id: uuid.UUID, service: EventService = Depends(get_event_service)):
    return await service.get_event(event_id)


@router.post("/{event_id}/sessions", response_model=SessionOut, status_code=201)
async def create_session(
    event_id: uuid.UUID,
    data: SessionCreate,
    current_user: User = Depends(require_role(UserRole.ORGANIZER)),
    service: EventService = Depends(get_event_service),
):
    return await service.create_session(event_id, data, current_user)