import pytest
from unittest.mock import AsyncMock
from datetime import date, timedelta
from app.services.invite_service import InviteService
from app.repositories.invite_repository import InviteRepository
from app.schemas.invite import InviteCreate
import uuid

@pytest.fixture
def fake_repo():
    return AsyncMock(spec=InviteRepository)

@pytest.mark.asyncio
async def test_create_invite_valide(fake_repo):
    service = InviteService(fake_repo)
    data = InviteCreate(
        nom="El Amrani",
        prenom="Khalid",
        fonction="Professeur",
        email="khalid@example.com",
        telephone="+212612345678",
        type_hebergement="Résidence",
        date_arrivee=date.today() + timedelta(days=10),
        date_depart=date.today() + timedelta(days=12)
    )
    demande_id=uuid.uuid4()
    fake_repo.create.return_value = {
        "id": uuid.uuid4(),
        "demande_id": demande_id,
        "nom": data.nom,
        "prenom": data.prenom,
        "fonction": data.fonction,
        "email": data.email,
        "telephone": data.telephone,
        "type_hebergement": data.type_hebergement,
        "date_arrivee": data.date_arrivee,
        "date_depart": data.date_depart
    }

    result = await service.add_invite(demande_id=demande_id, invite_data=data)
    assert isinstance(result.id, uuid.UUID)
    fake_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_dates_invite_invalides(fake_repo):
    service = InviteService(fake_repo)
    data = InviteCreate(
        nom="Dupont",
        prenom="Jean",
        fonction="Chargé de mission",
        email="jean@example.com",
        telephone="+212600000000",
        type_hebergement="Résidence",
        
        date_arrivee=date.today() + timedelta(days=5),
        date_depart=date.today() + timedelta(days=3)
    )
    demande_id=uuid.uuid4()
    with pytest.raises(ValueError, match="date d’arrivée doit être antérieure à la date de départ"):
        await service.add_invite(demande_id=demande_id, invite_data=data)
