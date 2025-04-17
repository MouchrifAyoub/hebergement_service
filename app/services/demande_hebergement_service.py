from datetime import date, timedelta
from typing import List, Optional
from uuid import UUID

from app.schemas.demande_hebergement import DemandeHebergementCreate, DemandeHebergementOut
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
from app.utils.logger import logger


class DemandeHebergementService:
    def __init__(self, repository: DemandeHebergementRepository):
        self.repository = repository

    async def create_demande(self, demande: DemandeHebergementCreate, demandeur_id: UUID) -> DemandeHebergementOut:
        logger.info(f"→ Demande dates : {demande.date_arrivee} → {demande.date_depart}")

        if demande.date_arrivee >= demande.date_depart:
            raise ValueError("La date d’arrivée doit être antérieure à la date de départ.")

        if demande.date_arrivee < date.today() + timedelta(days=10):
            raise ValueError("La demande doit être soumise au moins 10 jours avant la date d’arrivée.")

        has_duplicate = await self.repository.check_duplicate_period(
            demandeur_id,
            demande.date_arrivee,
            demande.date_depart
        )
        if has_duplicate:
            raise ValueError("Une autre demande active existe déjà pour cette période.")

        created = await self.repository.create(demande, demandeur_id)
        return DemandeHebergementOut(**created.__dict__)

    async def get_my_demandes(self, demandeur_id: UUID, statut: Optional[str] = None) -> List[DemandeHebergementOut]:
        demandes = await self.repository.get_all_by_demandeur_id(demandeur_id, statut)
        return [DemandeHebergementOut(**r._mapping) for r in demandes]

    async def update_demande(self, demande_id: UUID, demandeur_id: UUID, update_data: dict):
        demande = await self.repository.get_by_id_for_user(demande_id, demandeur_id)
        if demande is None:
            raise ValueError("Demande introuvable ou non autorisée.")

        if demande["statut"] != "EN_ATTENTE":
            raise ValueError("Seules les demandes en attente peuvent être modifiées.")

        if demande["code_ligne_budgetaire"]:
            raise ValueError("Impossible de modifier une demande déjà affectée à une ligne budgétaire.")

        return await self.repository.update_demande(demande_id, update_data)

    async def annuler_demande(self, demande_id: UUID, demandeur_id: UUID):
        demande = await self.repository.get_by_id_for_user(demande_id, demandeur_id)
        if demande is None:
            raise ValueError("Demande introuvable ou non autorisée.")

        if demande["statut"] != "EN_ATTENTE":
            raise ValueError("Seules les demandes en attente peuvent être annulées.")

        if demande["code_ligne_budgetaire"]:
            raise ValueError("Impossible d’annuler une demande déjà affectée à une ligne budgétaire.")

        return await self.repository.annuler_demande(demande_id)
