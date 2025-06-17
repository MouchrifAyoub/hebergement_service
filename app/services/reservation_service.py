from typing import List
from uuid import UUID
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.reservation import ReservationCreate, ReservationOut

class ReservationService:
    def __init__(self, repository: ReservationRepository):
        self.repository = repository

    async def create_reservation(self, data: ReservationCreate) -> ReservationOut:
        if data.date_depart <= data.date_arrivee:
            raise ValueError("La date de départ doit être postérieure à la date d’arrivée.")
        reservation = await self.repository.create(
            data.invite_id,
            data.date_arrivee,
            data.date_depart
        )
        return ReservationOut.model_validate(reservation)

    async def update_reservation_statut(self, reservation_id: UUID, statut: str) -> ReservationOut:
        reservation = await self.repository.update_statut(reservation_id, statut)
        if reservation is None:
            raise ValueError("Réservation introuvable")
        return ReservationOut.model_validate(reservation)

    async def get_reservations_by_invite(self, invite_id: UUID) -> List[ReservationOut]:
        reservations = await self.repository.get_by_invite_id(invite_id)
        return [ReservationOut.model_validate(r) for r in reservations]
