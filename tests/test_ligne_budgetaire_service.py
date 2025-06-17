import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from app.services.ligne_budgetaire_service import LigneBudgetaireService
from app.repositories.ligne_budgetaire_repository import LigneBudgetaireRepository
from app.schemas.ligne_budgetaire import LigneBudgetaireCreate

@pytest.fixture
def fake_repo():
    return AsyncMock(spec=LigneBudgetaireRepository)

@pytest.mark.asyncio
async def test_create_ligne_budgetaire_valide(fake_repo):
    service = LigneBudgetaireService(fake_repo)
    data = LigneBudgetaireCreate(
        code="BUDG-UNIT-001",
        description="Test via service",
        montant_disponible=10000.00
    )

    # Mock sous forme de dict attendu par LigneBudgetaireOut
    fake_repo.get_by_code.return_value = None
    fake_repo.create.return_value = {
        "id": uuid4(),
        "code": data.code,
        "description": data.description,
        "montant_disponible": data.montant_disponible
    }

    result = await service.create_ligne_budgetaire(data)
    assert result.code == data.code
    assert result.description == data.description
    assert result.montant_disponible == data.montant_disponible
    fake_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_creer_ligne_budgetaire_duplique(fake_repo):
    service = LigneBudgetaireService(fake_repo)
    data = LigneBudgetaireCreate(
        code="BUDG-UNIT-001",
        description="Duplique",
        montant_disponible=8000.00
    )
    
    # Simuler qu'un budget avec ce code existe déjà
    fake_repo.get_by_code.return_value = {
        "id": uuid4(),
        "code": data.code,
        "description": "Déjà existant",
        "montant_disponible": 9999.99
    }

    with pytest.raises(ValueError, match="existe déjà"):
        await service.create_ligne_budgetaire(data)
