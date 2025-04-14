from fastapi import APIRouter, Depends, HTTPException, status
from app.config.database import database
from app.schemas.demande_hebergement import DemandeHebergementCreate, DemandeHebergementOut
from app.services.demande_hebergement_service import DemandeHebergementService
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
from uuid import UUID

router = APIRouter()

@router.post("/demandes-hebergement", response_model=DemandeHebergementOut, status_code=status.HTTP_201_CREATED)
async def creer_demande_hebergement(
    payload: DemandeHebergementCreate,
    utilisateur_id: UUID = UUID("11111111-1111-1111-1111-111111111111")  #  À remplacer par un vrai système d'auth
):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    try:
        return await service.create_demande(payload, utilisateur_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
