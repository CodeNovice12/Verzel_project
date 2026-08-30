import uuid
import random
from fastapi import HTTPException, status

from app.domains.auth.models import User
from app.domains.events.models import Session, SessionMode
from app.domains.events.repository import SessionRepository
from app.domains.reservations.models import Reservation, ReservationStatus, SeatStatus
from app.domains.reservations.repository import SeatRepository, ReservationRepository
from app.domains.reservations.schemas import ReservationCreate


class ReservationService:
    def __init__(
        self,
        seat_repo: SeatRepository,
        reservation_repo: ReservationRepository,
        session_repo: SessionRepository,
    ):
        self.seat_repo = seat_repo
        self.reservation_repo = reservation_repo
        self.session_repo = session_repo

    async def create_reservation(
        self, data: ReservationCreate, customer: User
    ) -> Reservation:
        if data.seat_id:
            # No modo assento, busca a sessão normal
            session = await self.session_repo.get_by_id(data.session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Sessão não encontrada")
            return await self._reserve_seat(session, data.seat_id, customer)

        else:
            # No modo pista, busca a sessão com LOCK PESSIMISTA para serializar vendas concorrentes
            session = await self.session_repo.get_by_id_for_update(data.session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Sessão não encontrada")
            if data.quantity is None or data.quantity <= 0:
                raise HTTPException(
                    status_code=400, detail="Esta sessão exige uma quantidade válida"
                )
            return await self._reserve_quantity(session, data.quantity, customer)

    async def _reserve_seat(
        self, session: Session, seat_id: uuid.UUID, customer: User
    ) -> Reservation:
        seat = await self.seat_repo.get_by_id_for_update(seat_id)
        if seat is None or seat.session_id != session.id:
            raise HTTPException(status_code=404, detail="Assento não encontrado nesta sessão")
        if seat.status != SeatStatus.AVAILABLE:
            raise HTTPException(status_code=409, detail="Assento já reservado")

        reservation = Reservation(
            session_id=session.id,
            customer_id=customer.id,
            seat_id=seat.id,
            status=ReservationStatus.PENDING,
        )
        reservation = await self.reservation_repo.create(reservation)
        await self.seat_repo.update_status(seat, SeatStatus.RESERVED)
        return reservation

    async def _reserve_quantity(
        self, session: Session, quantity: int, customer: User
    ) -> Reservation:
        # A sessão está travada via FOR UPDATE. Nenhuma outra requisição calcula a contagem em paralelo.
        already_reserved = await self.reservation_repo.count_active_by_session(session.id)
        
        if already_reserved + quantity > session.capacity:
            raise HTTPException(
                status_code=409,
                detail=f"Capacidade insuficiente. Restam {session.capacity - already_reserved} lugares",
            )

        reservation = Reservation(
            session_id=session.id,
            customer_id=customer.id,
            quantity=quantity,
            status=ReservationStatus.PENDING,
        )
        return await self.reservation_repo.create(reservation)

    async def process_payment(self, reservation_id: uuid.UUID, customer: User) -> Reservation:
        reservation = await self.reservation_repo.get_by_id(reservation_id)
        if reservation is None:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        if reservation.customer_id != customer.id:
            raise HTTPException(status_code=403, detail="Essa reserva não é sua")
        if reservation.status != ReservationStatus.PENDING:
            raise HTTPException(
                status_code=409, detail=f"Reserva já está com status '{reservation.status.value}'"
            )

        approved = random.random() < 0.85

        reservation.status = (
            ReservationStatus.CONFIRMED if approved else ReservationStatus.CANCELLED
        )
        await self.reservation_repo.update_status(reservation)

        if not approved and reservation.seat_id:
            seat = await self.seat_repo.get_by_id_for_update(reservation.seat_id)
            if seat:
                await self.seat_repo.update_status(seat, SeatStatus.AVAILABLE)

        return reservation