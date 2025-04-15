from app.schemas.demande_hebergement import DemandeHebergementCreate, DemandeHebergementOut
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
from uuid import UUID
from typing import List, Optional
from datetime import date, timedelta


class DemandeHebergementService:
    def __init__(self, repository: DemandeHebergementRepository):
        self.repository = repository

    async def create_demande(self, demande: DemandeHebergementCreate, demandeur_id: UUID) -> DemandeHebergementOut:
        # TODO: remplacer par un vrai logger plus tard
        print("→ DATES :", demande.date_arrivee, demande.date_depart)

        # Validation des dates
        if demande.date_arrivee >= demande.date_depart:
            raise ValueError("La date d’arrivée doit être antérieure à la date de départ.")

        if demande.date_arrivee < date.today() + timedelta(days=10):
            raise ValueError("La demande doit être soumise au moins 10 jours avant la date d’arrivée.")

        # Vérification d’un doublon actif
        has_duplicate = await self.repository.check_duplicate_period(
            demandeur_id,
            demande.date_arrivee,
            demande.date_depart
        )
        if has_duplicate:
            raise ValueError("Une autre demande active existe déjà pour cette période.")

        # Création de la demande
        created = await self.repository.create(demande, demandeur_id)
        return DemandeHebergementOut(**created.__dict__)  # Tu peux aussi tester **created._mapping si besoin

    async def get_my_demandes(self, demandeur_id: UUID, statut: Optional[str] = None) -> List[DemandeHebergementOut]:
        demandes = await self.repository.get_all_by_demandeur_id(demandeur_id, statut)
        return [DemandeHebergementOut(**r._mapping) for r in demandes]
