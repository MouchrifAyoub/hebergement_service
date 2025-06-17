import pytest
from unittest.mock import AsyncMock
from datetime import date, timedelta
from uuid import uuid4
from app.services.reservation_service import ReservationService
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.reservation import ReservationCreate

@pytest.fixture
def fake_repo():
    return AsyncMock(spec=ReservationRepository)

@pytest.mark.asyncio
async def test_create_reservation_valide(fake_repo):
    service = ReservationService(fake_repo)

    data = ReservationCreate(
        invite_id=uuid4(),
        date_arrivee=date.today() + timedelta(days=10),
        date_depart=date.today() + timedelta(days=15),
        statut="CONFIRMEE"
    )

    fake_repo.create.return_value = {
        "id": uuid4(),
        "invite_id": data.invite_id,
        "date_arrivee": data.date_arrivee,
        "date_depart": data.date_depart,
        "statut": data.statut
    }

    result = await service.create_reservation(data)
    assert result.invite_id == data.invite_id
    fake_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_reservation_dates_invalides(fake_repo):
    service = ReservationService(fake_repo)

    data = ReservationCreate(
        invite_id=uuid4(),
        date_arrivee=date.today() + timedelta(days=7),
        date_depart=date.today() + timedelta(days=5),
        statut="CONFIRMEE"
    )

    with pytest.raises(ValueError, match="date de départ doit être postérieure à la date d’arrivée"):
        await service.create_reservation(data)
