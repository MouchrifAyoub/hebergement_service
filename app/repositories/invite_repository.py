import uuid
from typing import List
from uuid import UUID
from databases import Database
from sqlalchemy import select, insert
from sqlalchemy import and_
from app.models.invite import Invite
from app.config.settings import POSTGRES_SCHEMA

class InviteRepository:
    def __init__(self, db: Database):
        self.db = db
        self.schema = POSTGRES_SCHEMA

    async def create(self, demande_id: UUID, nom: str, prenom: str, fonction: str, date_arrivee, date_depart) -> Invite:
        query = insert(Invite).values(
            id=uuid.uuid4(),
            demande_id=demande_id,
            nom=nom,
            prenom=prenom,
            fonction=fonction,
            date_arrivee=date_arrivee,
            date_depart=date_depart
        ).returning(Invite)
        row = await self.db.fetch_one(query)
        return Invite(**row)

    async def get_by_demande_id(self, demande_id: UUID) -> List[Invite]:
        query = select(Invite).where(Invite.demande_id == demande_id)
        rows = await self.db.fetch_all(query)
        return [Invite(**r) for r in rows]
    
    async def check_disponibilite(self, type_hebergement: str, date_arrivee, date_depart) -> bool:
        query = f"""
            SELECT COUNT(*) FROM {self.schema}.invite
            WHERE type_hebergement = :type_hebergement
            AND (
                date_arrivee, date_depart
            ) OVERLAPS (
                :date_arrivee, :date_depart
            )
        """
        result = await self.db.fetch_val(query, {
            "type_hebergement": type_hebergement,
            "date_arrivee": date_arrivee,
            "date_depart": date_depart
        })
        return result == 0  # True si pas de chevauchement → dispo