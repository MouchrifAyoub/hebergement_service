from datetime import date, datetime
from typing import Optional, Literal
from uuid import UUID
from pydantic import BaseModel
import enum
from app.enums.statut_demande import StatutDemande



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

class TraitementDemandeIn(BaseModel):
    decision: Literal["VALIDEE", "REFUSEE"]
    hebergement_id: Optional[str] = None
    code_ligne_budgetaire: Optional[str] = None
    motif_refus: Optional[str] = None
    prise_en_charge_validee: Optional[bool] = None

class TraitementDemandeOut(BaseModel):
    id: str
    statut: str
    hebergement_id: Optional[str]
    code_ligne_budgetaire: Optional[str]
    prise_en_charge_validee: Optional[bool]
    motif_refus: Optional[str]