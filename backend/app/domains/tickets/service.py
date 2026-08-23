import uuid
from fastapi import HTTPException

from app.domains.tickets.models import Ticket, TicketStatus
from app.domains.tickets.repository import TicketRepository
from app.domains.tickets.security import sign_ticket_payload
from app.domains.reservations.repository import ReservationRepository
from app.domains.reservations.models import ReservationStatus
from app.domains.events.repository import SessionRepository
from app.domains.tickets.security import decode_ticket_payload
from app.domains.tickets.schemas import TicketValidationResult


class TicketService:
    def __init__(
        self,
        ticket_repo: TicketRepository,
        reservation_repo: ReservationRepository,
        session_repo: SessionRepository,
    ):
        self.ticket_repo = ticket_repo
        self.reservation_repo = reservation_repo
        self.session_repo = session_repo

    async def generate_for_reservation(self, reservation_id: uuid.UUID) -> Ticket:
        existing = await self.ticket_repo.get_by_reservation_id(reservation_id)
        if existing:
            return existing  # idempotente: não gera duplicado se já existe

        reservation = await self.reservation_repo.get_by_id(reservation_id)
        if reservation is None or reservation.status != ReservationStatus.CONFIRMED:
            raise HTTPException(
                status_code=400, detail="Reserva precisa estar confirmada para gerar ingresso"
            )

        session = await self.session_repo.get_by_id(reservation.session_id)

        ticket = Ticket(reservation_id=reservation.id, qr_signature="", status=TicketStatus.VALID)
        ticket = await self.ticket_repo.create(ticket)

        ticket.qr_signature = sign_ticket_payload(
            ticket_id=ticket.id,
            reservation_id=reservation.id,
            session_id=session.id,
            event_id=session.event_id,
        )
        return await self.ticket_repo.persist(ticket)

    async def list_my_tickets(self, customer_id: uuid.UUID) -> list[Ticket]:
        return await self.ticket_repo.list_by_customer(customer_id)
    
    async def validate_at_gate(self, code: str, session_id: uuid.UUID) -> TicketValidationResult:
        try:
            payload = decode_ticket_payload(code)
        except ValueError:
            return TicketValidationResult(result="invalid", message="QR inválido, corrompido ou forjado")

        ticket_id = uuid.UUID(payload["ticket_id"])
        ticket = await self.ticket_repo.get_by_id(ticket_id)

        if ticket is None:
            return TicketValidationResult(result="invalid", message="Ingresso não encontrado")

        if str(session_id) != payload["session_id"]:
            return TicketValidationResult(result="wrong_event", message="Ingresso não é desta sessão/evento")

        if ticket.status == TicketStatus.USED:
            return TicketValidationResult(result="already_used", message="Ingresso já foi utilizado")

        ticket.status = TicketStatus.USED
        await self.ticket_repo.persist(ticket)

        return TicketValidationResult(result="valid", message="Ingresso válido! Entrada liberada")