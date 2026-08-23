import uuid
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

    async def _get_session(self, session_id: uuid.UUID) -> Session:
        session = await self.session_repo.get_by_id(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        return session

    async def create_reservation(
        self, data: ReservationCreate, customer: User
    ) -> Reservation:
        session = await self._get_session(data.session_id)

        if session.mode == SessionMode.SEAT_MAP:
            if data.seat_id is None:
                raise HTTPException(
                    status_code=400, detail="Esta sessão exige seat_id (mapa de assentos)"
                )
            return await self._reserve_seat(session, data.seat_id, customer)

        else:  # SessionMode.QUANTITY
            if data.quantity is None:
                raise HTTPException(
                    status_code=400, detail="Esta sessão exige quantity (modo pista)"
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
        already_reserved = await self.reservation_repo.count_confirmed_by_session(session.id)
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