from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from typing import List

from app.config.database import database
from app.schemas.ligne_budgetaire import LigneBudgetaireCreate, LigneBudgetaireOut
from app.repositories.ligne_budgetaire_repository import LigneBudgetaireRepository
from app.services.ligne_budgetaire_service import LigneBudgetaireService

router = APIRouter()

@router.post("/ligne-budgetaire", response_model=LigneBudgetaireOut, status_code=status.HTTP_201_CREATED)
async def creer_ligne_budgetaire(
    payload: LigneBudgetaireCreate
):
    repository = LigneBudgetaireRepository(db=database)
    service = LigneBudgetaireService(repository)
    try:
        return await service.create_ligne_budgetaire(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/ligne-budgetaire/{code}", response_model=LigneBudgetaireOut)
async def get_ligne_budgetaire(code: str):
    repository = LigneBudgetaireRepository(db=database)
    service = LigneBudgetaireService(repository)
    try:
        return await service.get_ligne_by_code(code)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/ligne-budgetaire", response_model=List[LigneBudgetaireOut])
async def list_lignes_budgetaires():
    repository = LigneBudgetaireRepository(db=database)
    service = LigneBudgetaireService(repository)
    return await service.get_all()

@router.put("/ligne-budgetaire/{code}/montant", response_model=LigneBudgetaireOut)
async def update_montant_ligne_budgetaire(code: str, montant: float = Body(...)):
    repository = LigneBudgetaireRepository(db=database)
    service = LigneBudgetaireService(repository)
    try:
        return await service.update_montant(code, montant)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))