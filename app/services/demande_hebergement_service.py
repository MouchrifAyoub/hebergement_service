from fastapi import HTTPException
from datetime import date, timedelta
from app.schemas.demande_hebergement import DemandeHebergementCreate
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
from app.schemas.demande_hebergement import DemandeHebergementOut
from uuid import UUID

class DemandeHebergementService:
    def __init__(self, repository: DemandeHebergementRepository):
        self.repository = repository

    async def create_demande(self, demande: DemandeHebergementCreate, demandeur_id: UUID) -> DemandeHebergementOut:
        print("→ DATES :", demande.date_arrivee, demande.date_depart)
        # Validation dates
        if demande.date_arrivee >= demande.date_depart:
            raise ValueError("La date d’arrivée doit être antérieure à la date de départ.")
        
        if demande.date_arrivee < date.today() + timedelta(days=10):
            raise ValueError("La demande doit être soumise au moins 10 jours avant la date d’arrivée.")

        # Vérification chevauchement
        has_duplicate = await self.repository.check_duplicate_period(
            demandeur_id,
            demande.date_arrivee,
            demande.date_depart
        )
        if has_duplicate:
            raise ValueError("Une autre demande active existe déjà pour cette période.")

        # Création
        created = await self.repository.create(demande, demandeur_id)
        return DemandeHebergementOut(**created.__dict__)
