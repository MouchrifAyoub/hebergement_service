import pytest
from datetime import date, timedelta
import uuid

@pytest.mark.asyncio
async def test_create_reservation(async_client):
    # Étape 1 : créer une demande valide
    demande_payload = {
        "date_arrivee": str(date.today() + timedelta(days=10)),
        "date_depart": str(date.today() + timedelta(days=15)),
        "motif": "Formation"
    }
    demandeur_id = str(uuid.uuid4())
    demande_response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=demande_payload
    )
    assert demande_response.status_code == 201
    demande_id = demande_response.json()["id"]

    # Étape 2 : créer un invité lié à cette demande
    invite_payload = {
        "nom": "Test",
        "prenom": "Invité",
        "fonction": "Développeur",
        "email": f"invite_{uuid.uuid4().hex[:6]}@example.com",
        "telephone": "0600000000",
        "type_hebergement": "Hôtel",
        "date_arrivee": str(date.today() + timedelta(days=10)),
        "date_depart": str(date.today() + timedelta(days=12))
    }
    invite_response = await async_client.post(
        f"/invites/reservations-invites?demande_id={demande_id}",
        json=invite_payload
    )
    assert invite_response.status_code == 201
    invite_id = invite_response.json()["id"]

    # Étape 3 : créer une réservation liée à l’invité
    reservation_payload = {
        "invite_id": invite_id,
        "date_arrivee": invite_payload["date_arrivee"],
        "date_depart": invite_payload["date_depart"]
    }
    response = await async_client.post("/hebergement/reservations", json=reservation_payload)
    print("→ RESERVATION RESPONSE STATUS:", response.status_code)
    print("→ RESERVATION RESPONSE BODY:", response.text)
    assert response.status_code in (200, 201)


@pytest.mark.asyncio
async def test_reservation_dates_invalides(async_client):
    # Étape 1 : créer une demande valide
    demande_payload = {
        "date_arrivee": str(date.today() + timedelta(days=15)),
        "date_depart": str(date.today() + timedelta(days=20)),
        "motif": "Test demande"
    }
    demandeur_id = str(uuid.uuid4())
    demande_response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=demande_payload
    )
    assert demande_response.status_code == 201
    demande_id = demande_response.json()["id"]

    # Étape 2 : créer un invité lié à cette demande
    invite_payload = {
        "nom": "Test",
        "prenom": "Invité",
        "fonction": "Testeur",
        "email": f"invite_{uuid.uuid4().hex[:6]}@example.com",
        "telephone": "0600000000",
        "type_hebergement": "Hôtel",
        "date_arrivee": str(date.today() + timedelta(days=16)),
        "date_depart": str(date.today() + timedelta(days=18))
    }
    invite_response = await async_client.post(
        f"/invites/reservations-invites?demande_id={demande_id}",
        json=invite_payload
    )
    assert invite_response.status_code == 201
    invite_id = invite_response.json()["id"]

    # Étape 3 : tentative de réservation avec dates invalides
    reservation_payload = {
        "invite_id": invite_id,
        "date_arrivee": str(date.today() + timedelta(days=20)),
        "date_depart": str(date.today() + timedelta(days=18))
    }
    response = await async_client.post("/hebergement/reservations", json=reservation_payload)
    assert response.status_code in (400, 422)
