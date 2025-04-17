from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
import enum


class StatutDemande(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VALIDEE = "VALIDEE"
    REFUSEE = "REFUSEE"
    ANNULEE = "ANNULEE"
    ARCHIVEE = "ARCHIVEE"


class DemandeHebergementCreate(BaseModel):
    date_arrivee: date
    date_depart: date
    motif: str
    justificatif_url: Optional[str] = None


class DemandeHebergementOut(BaseModel):
    id: UUID
    date_soumission: datetime
    date_arrivee: date
    date_depart: date
    motif: str
    justificatif_url: Optional[str]
    statut: StatutDemande
    code_ligne_budgetaire: Optional[str]
    demandeur_id: UUID

    model_config = {
        "from_attributes": True
    }


class DemandeHebergementUpdate(BaseModel):
    """
    Champs modifiables d'une demande d'hébergement tant qu'elle est en attente.
    """
    date_arrivee: Optional[date] = None
    date_depart: Optional[date] = None
    motif: Optional[str] = None
    justificatif_url: Optional[str] = None
