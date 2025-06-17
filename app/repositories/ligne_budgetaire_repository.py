import uuid
from typing import Optional
from uuid import UUID
from databases import Database
from sqlalchemy import select, insert, update

from app.models.ligne_budgetaire import LigneBudgetaire
from app.config.settings import POSTGRES_SCHEMA

class LigneBudgetaireRepository:
    def __init__(self, db: Database):
        self.db = db
        self.schema = POSTGRES_SCHEMA

    async def create(self, code: str, description: str, montant_disponible) -> LigneBudgetaire:
        query = insert(LigneBudgetaire).values(
            id=uuid.uuid4(),
            code=code,
            description=description,
            montant_disponible=montant_disponible
        ).returning(LigneBudgetaire)
        row = await self.db.fetch_one(query)
        return LigneBudgetaire(**row)

    async def get_by_code(self, code: str) -> Optional[LigneBudgetaire]:
        query = select(LigneBudgetaire).where(LigneBudgetaire.code == code)
        row = await self.db.fetch_one(query)
        return LigneBudgetaire(**row) if row else None

    async def update_montant(self, code: str, new_montant):
        query = update(LigneBudgetaire).where(
            LigneBudgetaire.code == code
        ).values(
            montant_disponible=new_montant
        ).returning(LigneBudgetaire)
        row = await self.db.fetch_one(query)
        return LigneBudgetaire(**row) if row else None
    
    async def get_all(self):
        query = select(LigneBudgetaire)
        return await self.db.fetch_all(query)
