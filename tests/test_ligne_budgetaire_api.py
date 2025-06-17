import pytest
from datetime import datetime
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_ligne_budgetaire(async_client):
    code = f"BUDG-{uuid4().hex[:8]}"
    payload = {
        "code": code,
        "description": "Test budget auto",
        "montant_disponible": 5000.00
    }
    response = await async_client.post("/hebergement/ligne-budgetaire", json=payload)
    print("→ RESPONSE STATUS:", response.status_code)
    print("→ RESPONSE BODY:", response.text)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == payload["code"]
    assert float(data["montant_disponible"]) == payload["montant_disponible"]

@pytest.mark.asyncio
async def test_ligne_budgetaire_code_duplique(async_client):
    # Même payload que précédemment (code identique = duplication)
    payload = {
        "code": "BUDG-TEST-001",
        "description": "Budget doublon",
        "montant_disponible": 1000.00
    }
    response = await async_client.post("/hebergement/ligne-budgetaire", json=payload)
    assert response.status_code in (400, 422)


@pytest.mark.asyncio
async def test_update_montant_ligne_budgetaire(async_client):
    code = f"BUDG-{uuid4().hex[:8]}"
    payload = {
        "code": code,
        "description": "Test montant update",
        "montant_disponible": 2000.00
    }

    # Créer une ligne
    response = await async_client.post("/hebergement/ligne-budgetaire", json=payload)
    assert response.status_code == 201

    # Mise à jour du montant
    update_response = await async_client.put(
        f"/hebergement/ligne-budgetaire/{code}/montant",
        json=3000.00
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert float(data["montant_disponible"]) == 3000.00
