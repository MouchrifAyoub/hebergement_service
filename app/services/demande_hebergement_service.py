from datetime import date, timedelta
from typing import List, Optional
from uuid import UUID

from app.schemas.demande_hebergement import DemandeHebergementCreate, DemandeHebergementOut, TraitementDemandeIn
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
    
    async def traiter_demande(self, demande_id: UUID, data: TraitementDemandeIn):
        demande = await self.repository.get_by_id(demande_id)
        if not demande:
            raise ValueError("Demande introuvable.")

        if demande["statut"] != "EN_ATTENTE":
            raise ValueError("La demande a déjà été traitée.")

        # Vérification métier
        if data.decision == "REFUSEE" and not data.motif_refus:
            raise ValueError("Un motif est requis pour refuser une demande.")

        if data.decision == "VALIDEE":
            if not data.prise_en_charge_validee and not data.code_ligne_budgetaire:
                raise ValueError("Aucune prise en charge. Ligne budgétaire obligatoire.")

        # Mise à jour de la demande
        update_data = {
            "statut": data.decision,
            "hebergement_id": data.hebergement_id,
            "code_ligne_budgetaire": data.code_ligne_budgetaire,
            "prise_en_charge_validee": data.prise_en_charge_validee,
            "motif_refus": data.motif_refus
        }

        updated = await self.repository.update_demande(demande_id, update_data)

        if updated is None:
            raise ValueError("Demande non trouvée")

        updated_dict = dict(updated)  # ou parse_obj(updated)
        return DemandeHebergementOut(**updated_dict)
    
    async def get_demandes_en_attente(self):
        return await self.repository.get_demandes_en_attente()