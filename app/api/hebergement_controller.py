from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List, Optional

from app.config.database import database
from app.schemas.demande_hebergement import DemandeHebergementCreate, DemandeHebergementOut
from app.services.demande_hebergement_service import DemandeHebergementService
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository

router = APIRouter()

# ⚠️ Temporaire : ID codé en dur, à remplacer par une dépendance d'auth plus tard
UTILISATEUR_ID_TEST = UUID("11111111-1111-1111-1111-111111111111")

@router.post("/demandes-hebergement", response_model=DemandeHebergementOut, status_code=status.HTTP_201_CREATED)
async def creer_demande_hebergement(
    payload: DemandeHebergementCreate,
    utilisateur_id: UUID = UTILISATEUR_ID_TEST
):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    try:
        return await service.create_demande(payload, utilisateur_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/mes-demandes-hebergement", response_model=List[DemandeHebergementOut])
async def get_mes_demandes(statut: Optional[str] = None):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    demandes = await service.get_my_demandes(UTILISATEUR_ID_TEST, statut)
    print(f"{len(demandes)} demandes trouvées pour {UTILISATEUR_ID_TEST} (statut={statut})")
    return demandes
