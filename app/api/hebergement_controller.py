from fastapi import APIRouter, Depends, HTTPException, status, Path, Body, Query
from uuid import UUID
from typing import List, Optional

from app.config.database import database
from app.schemas.demande_hebergement import (
    DemandeHebergementCreate,
    DemandeHebergementOut,
    DemandeHebergementUpdate,
    TraitementDemandeIn
)
from app.services.demande_hebergement_service import DemandeHebergementService
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
# from app.utils.logger import logger  # si logger utilisé

router = APIRouter()

UTILISATEUR_ID_TEST = UUID("11111111-1111-1111-1111-111111111111")


@router.post("/demandes-hebergement", response_model=DemandeHebergementOut, status_code=status.HTTP_201_CREATED)
async def creer_demande_hebergement(
    payload: DemandeHebergementCreate,
    demandeur_id: UUID  # doit être passé en query param
):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    try:
        return await service.create_demande(payload, demandeur_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/mes-demandes-hebergement", response_model=List[DemandeHebergementOut])
async def get_mes_demandes(statut: Optional[str] = None):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    demandes = await service.get_my_demandes(UTILISATEUR_ID_TEST, statut)
    # logger.info(...) si logger
    return demandes


@router.put("/demandes-hebergement/{id}", response_model=DemandeHebergementOut)
async def update_demande_hebergement(
    id: UUID = Path(...),
    payload: DemandeHebergementUpdate = Body(...),
    demandeur_id: UUID = Query(...),  # ✅ récupérer le bon ID transmis
):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    try:
        data = {k: v for k, v in payload.model_dump().items() if v is not None}
        return await service.update_demande(id, demandeur_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/demandes-hebergement/{id}")
async def annuler_demande_hebergement(id: UUID = Path(...)):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    utilisateur_id = UTILISATEUR_ID_TEST
    try:
        result = await service.annuler_demande(id, utilisateur_id)
        return {"message": "Demande annulée avec succès", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/traiter-demande/{id}", response_model=DemandeHebergementOut)
async def traiter_demande(
    id: UUID = Path(...),
    payload: TraitementDemandeIn = Body(...),
):
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    try:
        return await service.traiter_demande(id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/demandes-en-attente", response_model=List[DemandeHebergementOut])
async def get_demandes_en_attente():
    repository = DemandeHebergementRepository(db=database)
    service = DemandeHebergementService(repository)
    demandes = await service.get_demandes_en_attente()
    return [DemandeHebergementOut(**dict(d)) for d in demandes]
