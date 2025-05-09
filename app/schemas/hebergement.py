from uuid import UUID
from enum import Enum
from pydantic import BaseModel

class TypeHebergement(str, Enum):
    CHAMBRE = "CHAMBRE"
    SUITE = "SUITE"
    HILTON = "HILTON"
    CLUB_DE_TIR = "CLUB_DE_TIR"

class HebergementCreate(BaseModel):
    nom: str
    type: TypeHebergement
    disponible: bool = True

class HebergementOut(BaseModel):
    id: UUID
    nom: str
    type: TypeHebergement
    disponible: bool

    model_config = {
        "from_attributes": True
    }
