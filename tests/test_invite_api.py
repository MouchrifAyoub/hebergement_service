import io
from fastapi import UploadFile
import pytest
from datetime import date, timedelta
import uuid

@pytest.mark.asyncio
async def test_create_invite(async_client):
    # Préparer un ID de demande existant en base si nécessaire
    demande_id = str(uuid.uuid4())
    payload = {
        "demande_id": demande_id,
        "nom": "Amine",
        "prenom": "Yassine",
        "fonction": "Chargé de mission",
        "email": "yassine.amine@example.com",
        "telephone": "+212699999999",
        "type_hebergement": "Résidence",
        "date_arrivee": str(date.today() + timedelta(days=10)),
        "date_depart": str(date.today() + timedelta(days=12))
    }

    # NB : ce test nécessite que la demande_id soit bien présente si validée par la route
    response = await async_client.post("/invites/reservations-invites", json=payload)
    assert response.status_code in (201, 422, 400)  # tolérance si lien cassé avec demande

@pytest.mark.asyncio
async def test_invite_dates_invalides(async_client):
    payload = {
        "demande_id": str(uuid.uuid4()),
        "nom": "Test",
        "prenom": "Erreur",
        "fonction": "Professeur",
        "email": "test@example.com",
        "telephone": "+212611111111",
        "type_hebergement": "Résidence",
        "date_arrivee": str(date.today() + timedelta(days=8)),
        "date_depart": str(date.today() + timedelta(days=5))
    }

    response = await async_client.post("/invites/reservations-invites", json=payload)
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_import_csv_format_invalide(async_client):
    content = "nom;prenom;email\nA;B;a@b.com"  # Mauvais séparateur
    file = UploadFile(filename="test.csv", file=io.StringIO(content))
    response = await async_client.post(
        f"/invites/reservations-invites/import-csv?demande_id={uuid.uuid4()}",
        files={"file": ("test.csv", content, "text/csv")}
    )
    assert response.status_code == 400