import pytest
from datetime import date, timedelta
import sys
import os
import uuid
import random
from uuid import UUID

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.demande_hebergement import StatutDemande


@pytest.mark.asyncio
async def test_create_demande_valide(async_client):
    payload = {
        "date_arrivee": str(date.today() + timedelta(days=15)),
        "date_depart": str(date.today() + timedelta(days=20)),
        "motif": "Participation à une conférence",
        "justificatif_url": "https://example.com/justificatif.pdf"
    }

    demandeur_id = uuid.uuid4()
    response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["motif"] == payload["motif"]
    assert data["statut"] == StatutDemande.EN_ATTENTE
    assert data["demandeur_id"] == str(demandeur_id)


@pytest.mark.asyncio
async def test_refus_date_invalide(async_client):
    payload = {
        "date_arrivee": str(date.today() + timedelta(days=10)),
        "date_depart": str(date.today() + timedelta(days=5)),
        "motif": "Date invalide"
    }

    demandeur_id = uuid.uuid4()
    response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=payload
    )

    assert response.status_code == 400
    assert "date d’arrivée doit être antérieure" in response.text

@pytest.mark.asyncio
async def test_get_mes_demandes(async_client):
    # On suppose qu’il y a déjà au moins une demande créée avec cet utilisateur
    utilisateur_id = uuid.UUID("11111111-1111-1111-1111-111111111111")

    response = await async_client.get("/hebergement/mes-demandes-hebergement")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Optionnel : vérifier la structure
    if data:
        assert "id" in data[0]
        assert "statut" in data[0]
        assert data[0]["demandeur_id"] == str(utilisateur_id)

@pytest.mark.asyncio
async def test_traiter_demande_valider(async_client):
    # Prérequis : création d’une demande valide à traiter
    creation_payload = {
        "date_arrivee": str(date.today() + timedelta(days=15)),
        "date_depart": str(date.today() + timedelta(days=20)),
        "motif": "Participation à un atelier",
        "justificatif_url": None
    }

    demandeur_id = uuid.uuid4()
    create_response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=creation_payload
    )

    assert create_response.status_code == 201
    demande_id = create_response.json()["id"]

    # Traitement administratif : validation avec prise en charge
    traitement_payload = {
        "decision": "VALIDEE",
        "prise_en_charge_validee": True,
        "code_ligne_budgetaire": "BUDG-2025-01"
    }

    traiter_response = await async_client.put(
        f"/hebergement/traiter-demande/{demande_id}",
        json=traitement_payload
    )

    assert traiter_response.status_code == 200
    result = traiter_response.json()
    assert result["statut"] == "VALIDEE"
    assert result["code_ligne_budgetaire"] == "BUDG-2025-01"

@pytest.mark.asyncio
async def test_update_demande(async_client):
    offset = random.randint(100, 200)
    demandeur_id = uuid.uuid4()

    # Création de la demande
    payload = {
        "date_arrivee": str(date.today() + timedelta(days=offset)),
        "date_depart": str(date.today() + timedelta(days=offset + 5)),
        "motif": "Mission professionnelle"
    }

    create_response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=payload
    )

    print("→ CREATE STATUS:", create_response.status_code)
    print("→ CREATE BODY:", create_response.text)
    assert create_response.status_code == 201, f"Échec création: {create_response.text}"

    demande = create_response.json()
    assert demande["statut"] == "EN_ATTENTE"

    # ✅ Conversion correcte du demandeur_id pour éviter erreur de type
    actual_demandeur_id = UUID(demande["demandeur_id"])

    # Mise à jour
    update_payload = {
        "motif": "Mission prolongée"
    }

    update_response = await async_client.put(
        f"/hebergement/demandes-hebergement/{demande['id']}?demandeur_id={actual_demandeur_id}",
        json=update_payload
    )

    print("→ UPDATE STATUS:", update_response.status_code)
    print("→ UPDATE BODY:", update_response.text)
    assert update_response.status_code == 200, f"Échec update: {update_response.text}"

    updated = update_response.json()
    assert updated["motif"] == "Mission prolongée"
    assert updated["id"] == demande["id"]



@pytest.mark.asyncio
async def test_annuler_demande(async_client):
    # Étape 1 : Créer une demande en attente
    demandeur_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    payload = {
        "date_arrivee": str(date.today() + timedelta(days=60)),
        "date_depart": str(date.today() + timedelta(days=65)),
        "motif": "Séminaire"
    }

    create_response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=payload
    )
    print("→ CREATE STATUS:", create_response.status_code)
    print("→ CREATE BODY:", create_response.text)
    assert create_response.status_code == 201

    demande = create_response.json()
    assert demande["statut"] == "EN_ATTENTE"
    demande_id = demande["id"]

    # Étape 2 : Annuler la demande
    delete_response = await async_client.delete(
        f"/hebergement/demandes-hebergement/{demande_id}"
    )
    print("→ DELETE STATUS:", delete_response.status_code)
    print("→ DELETE BODY:", delete_response.text)
    assert delete_response.status_code == 200

    result = delete_response.json()
    assert result["message"] == "Demande annulée avec succès"
    assert result["data"]["statut"] == "ANNULEE"



@pytest.mark.asyncio
async def test_traiter_demande_refusee_sans_motif(async_client):
    # Préparation
    payload = {
        "date_arrivee": str(date.today() + timedelta(days=15)),
        "date_depart": str(date.today() + timedelta(days=20)),
        "motif": "Test refus sans motif"
    }
    demandeur_id = uuid.uuid4()
    response = await async_client.post(
        f"/hebergement/demandes-hebergement?demandeur_id={demandeur_id}",
        json=payload
    )
    assert response.status_code == 201
    demande_id = response.json()["id"]

    # Traitement refusé sans motif
    traitement = {
        "decision": "REFUSEE",
        "motif_refus": None
    }

    traitement_response = await async_client.put(
        f"/hebergement/traiter-demande/{demande_id}",
        json=traitement
    )

    assert traitement_response.status_code == 400
    assert "motif est requis pour refuser" in traitement_response.text
