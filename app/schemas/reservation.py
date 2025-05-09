from datetime import date
from uuid import UUID
from pydantic import BaseModel

class ReservationCreate(BaseModel):
    invite_id: UUID
    date_arrivee: date
    date_depart: date

class ReservationOut(BaseModel):
    id: UUID
    invite_id: UUID
    date_arrivee: date
    date_depart: date
    statut: str

    model_config = {
        "from_attributes": True
    }
