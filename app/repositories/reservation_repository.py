import uuid
from databases import Database
from sqlalchemy import select, insert, update
from uuid import UUID
from typing import List, Optional

from app.models.reservation import Reservation
from app.config.settings import POSTGRES_SCHEMA

class ReservationRepository:
    def __init__(self, db: Database):
        self.db = db
        self.schema = POSTGRES_SCHEMA

    async def create(self, invite_id: UUID, date_arrivee, date_depart) -> Reservation:
        query = insert(Reservation).values(
            id=uuid.uuid4(),
            invite_id=invite_id,
            date_arrivee=date_arrivee,
            date_depart=date_depart,
            statut='CONFIRMEE'
        ).returning(Reservation)
        row = await self.db.fetch_one(query)
        return Reservation(**row)

    async def update_statut(self, reservation_id: UUID, statut: str):
        query = update(Reservation).where(
            Reservation.id == reservation_id
        ).values(statut=statut).returning(Reservation)
        row = await self.db.fetch_one(query)
        return Reservation(**row) if row else None

    async def get_by_invite_id(self, invite_id: UUID) -> List[Reservation]:
        query = select(Reservation).where(Reservation.invite_id == invite_id)
        rows = await self.db.fetch_all(query)
        return [Reservation(**r) for r in rows]
