from fastapi import APIRouter, HTTPException, status, Path, Body
from uuid import UUID
from typing import List

from app.config.database import database
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.repositories.reservation_repository import ReservationRepository
from app.services.reservation_service import ReservationService

router = APIRouter()

@router.post("/reservations", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def creer_reservation(payload: ReservationCreate):
    repository = ReservationRepository(db=database)
    service = ReservationService(repository)
    try:
        return await service.create_reservation(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/reservations/{id}", response_model=ReservationOut)
async def modifier_statut_reservation(id: UUID, statut: str = Body(...)):
    repository = ReservationRepository(db=database)
    service = ReservationService(repository)
    try:
        return await service.update_reservation_statut(id, statut)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/reservations/invite/{invite_id}", response_model=List[ReservationOut])
async def lister_reservations(invite_id: UUID):
    repository = ReservationRepository(db=database)
    service = ReservationService(repository)
    return await service.get_reservations_by_invite(invite_id)
