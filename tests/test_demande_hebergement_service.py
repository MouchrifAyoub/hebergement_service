import pytest
from datetime import date, timedelta
from uuid import uuid4

from app.services.demande_hebergement_service import DemandeHebergementService
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
from app.schemas.demande_hebergement import DemandeHebergementCreate
from app.models.demande_hebergement import StatutDemande
from unittest.mock import AsyncMock


@pytest.fixture
def fake_repo():
    repo = AsyncMock(spec=DemandeHebergementRepository)
    repo.check_duplicate_period.return_value = False
    return repo


@pytest.mark.asyncio
async def test_create_demande_valide(fake_repo):
    service = DemandeHebergementService(fake_repo)
    demande_data = DemandeHebergementCreate(
        date_arrivee=date.today() + timedelta(days=15),
        date_depart=date.today() + timedelta(days=20),
        motif="Participation à un séminaire",
        justificatif_url="https://example.com/justificatif.pdf"
    )
    demandeur_id = uuid4()

    # Simulation de retour du repository
    fake_repo.create.return_value = {
        "id": uuid4(),
        "date_soumission": date.today(),
        "date_arrivee": demande_data.date_arrivee,
        "date_depart": demande_data.date_depart,
        "motif": demande_data.motif,
        "justificatif_url": demande_data.justificatif_url,
        "statut": "EN_ATTENTE",
        "code_ligne_budgetaire": None,
        "demandeur_id": demandeur_id
    }

    result = await service.create_demande(demande_data, demandeur_id)
    assert result.date_arrivee == demande_data.date_arrivee
    assert result.motif == demande_data.motif
    assert result.statut.value == StatutDemande.EN_ATTENTE.value


@pytest.mark.asyncio
async def test_refus_date_invalide(fake_repo):
    service = DemandeHebergementService(fake_repo)
    demande_data = DemandeHebergementCreate(
        date_arrivee=date.today() + timedelta(days=10),
        date_depart=date.today() + timedelta(days=5),  # Invalide
        motif="Erreur de date"
    )
    demandeur_id = uuid4()

    with pytest.raises(ValueError, match="date d’arrivée doit être antérieure à la date de départ"):
        await service.create_demande(demande_data, demandeur_id)


@pytest.mark.asyncio
async def test_refus_date_trop_proche(fake_repo):
    service = DemandeHebergementService(fake_repo)
    demande_data = DemandeHebergementCreate(
        date_arrivee=date.today() + timedelta(days=3),  # Trop proche
        date_depart=date.today() + timedelta(days=5),
        motif="Visite"
    )
    demandeur_id = uuid4()

    with pytest.raises(ValueError, match="doit être soumise au moins 10 jours avant"):
        await service.create_demande(demande_data, demandeur_id)


@pytest.mark.asyncio
async def test_refus_demande_dupliquee(fake_repo):
    fake_repo.check_duplicate_period.return_value = True
    service = DemandeHebergementService(fake_repo)

    demande_data = DemandeHebergementCreate(
        date_arrivee=date.today() + timedelta(days=15),
        date_depart=date.today() + timedelta(days=20),
        motif="Conférence"
    )
    demandeur_id = uuid4()

    with pytest.raises(ValueError, match="demande active existe déjà pour cette période"):
        await service.create_demande(demande_data, demandeur_id)


@pytest.mark.asyncio
async def test_traitement_valide_sans_PEC_ni_budget(fake_repo):
    from app.schemas.demande_hebergement import TraitementDemandeIn
    service = DemandeHebergementService(fake_repo)

    fake_repo.get_by_id.return_value = {
        "id": uuid4(),
        "statut": "EN_ATTENTE"
    }

    traitement_data = TraitementDemandeIn(
        decision="VALIDEE",
        prise_en_charge_validee=False,
        code_ligne_budgetaire=None
    )

    with pytest.raises(ValueError, match="Ligne budgétaire obligatoire"):
        await service.traiter_demande(uuid4(), traitement_data)


@pytest.mark.asyncio
async def test_traitement_refuse_sans_motif(fake_repo):
    from app.schemas.demande_hebergement import TraitementDemandeIn
    service = DemandeHebergementService(fake_repo)

    fake_repo.get_by_id.return_value = {
        "id": uuid4(),
        "statut": "EN_ATTENTE"
    }

    traitement_data = TraitementDemandeIn(
        decision="REFUSEE",
        motif_refus=None
    )

    with pytest.raises(ValueError, match="motif est requis pour refuser"):
        await service.traiter_demande(uuid4(), traitement_data)
