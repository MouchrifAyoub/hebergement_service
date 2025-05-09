from fastapi import APIRouter, Depends, HTTPException, status, Path, Body, UploadFile, File
from uuid import UUID
from typing import List

from app.config.database import database
from app.schemas.invite import InviteCreate, InviteOut
from app.repositories.invite_repository import InviteRepository
from app.services.invite_service import InviteService

router = APIRouter()

@router.post("/reservations-invites", response_model=InviteOut, status_code=status.HTTP_201_CREATED)
async def ajouter_invite(
    demande_id: UUID,
    payload: InviteCreate
):
    repository = InviteRepository(db=database)
    service = InviteService(repository)
    try:
        return await service.add_invite(demande_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/reservations-invites/{demande_id}", response_model=List[InviteOut])
async def lister_invites(demande_id: UUID):
    repository = InviteRepository(db=database)
    service = InviteService(repository)
    return await service.get_invites_for_demande(demande_id)

@router.post("/reservations-invites/import-csv")
async def importer_invites_csv(demande_id: UUID, file: UploadFile = File(...)):
    repository = InviteRepository(db=database)
    service = InviteService(repository)
    try:
        invites = await service.import_from_csv(demande_id, file)
        return {"message": f"{len(invites)} invités importés avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
