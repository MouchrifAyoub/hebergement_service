from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal

class LigneBudgetaireCreate(BaseModel):
    code: str
    description: str
    montant_disponible: Decimal

class LigneBudgetaireOut(BaseModel):
    id: UUID
    code: str
    description: str
    montant_disponible: Decimal

    model_config = {
        "from_attributes": True
    }
