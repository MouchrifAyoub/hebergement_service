from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ReservationCreate(BaseModel):
    invite_id: UUID
    date_arrivee: date
    date_depart: date
    statut: Optional[str] = "CONFIRMEE"

class ReservationOut(BaseModel):
    id: UUID
    invite_id: UUID
    date_arrivee: date
    date_depart: date
    statut: str

    model_config = {
        "from_attributes": True
    }
