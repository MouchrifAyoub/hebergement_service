from datetime import date
from uuid import UUID
from pydantic import BaseModel
from app.enums.type_hebergement import TypeHebergement


class InviteCreate(BaseModel):
    nom: str
    prenom: str
    fonction: str
    date_arrivee: date
    date_depart: date
    email: str
    telephone: str
    type_hebergement: str

class InviteOut(BaseModel):
    id: UUID
    demande_id: UUID
    nom: str
    prenom: str
    fonction: str
    email: str
    telephone: str
    type_hebergement: TypeHebergement
    date_arrivee: date
    date_depart: date

    model_config = {
        "from_attributes": True
    }
