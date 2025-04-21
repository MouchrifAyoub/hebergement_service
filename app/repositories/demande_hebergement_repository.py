from datetime import datetime
from typing import Optional, List
from uuid import UUID
import uuid
import logging

from databases import Database
from sqlalchemy import select, and_, insert

from app.config.settings import POSTGRES_SCHEMA
from app.models.demande_hebergement import DemandeHebergement, StatutDemande
from app.schemas.demande_hebergement import DemandeHebergementCreate

logger = logging.getLogger(__name__)


class DemandeHebergementRepository:
    def __init__(self, db: Database):
        self.db = db
        self.schema = POSTGRES_SCHEMA

    async def create(self, demande: DemandeHebergementCreate, demandeur_id: UUID) -> DemandeHebergement:
        query = insert(DemandeHebergement).values(
            id=uuid.uuid4(),
            date_soumission=datetime.utcnow(),
            date_arrivee=demande.date_arrivee,
            date_depart=demande.date_depart,
            motif=demande.motif,
            justificatif_url=demande.justificatif_url,
            statut=StatutDemande.EN_ATTENTE,
            code_ligne_budgetaire=None,
            demandeur_id=demandeur_id
        ).returning(DemandeHebergement)

        row = await self.db.fetch_one(query)
        return DemandeHebergement(**row)

    async def check_duplicate_period(self, demandeur_id: UUID, date_arrivee, date_depart) -> bool:
        query = select(DemandeHebergement).where(
            and_(
                DemandeHebergement.demandeur_id == demandeur_id,
                DemandeHebergement.statut.in_([
                    StatutDemande.EN_ATTENTE.value,
                    StatutDemande.VALIDEE.value
                ]),
                DemandeHebergement.date_arrivee < date_depart,
                DemandeHebergement.date_depart > date_arrivee
            )
        )
        logger.info("→ Vérification d'une demande existante...")
        result = await self.db.fetch_one(query)
        logger.info(f"→ Résultat trouvé : {result}")
        return result is not None

    async def get_all_by_demandeur_id(self, demandeur_id: UUID, statut: Optional[str] = None) -> List[DemandeHebergement]:
        query = select(DemandeHebergement).where(DemandeHebergement.demandeur_id == demandeur_id)

        if statut:
            query = query.where(DemandeHebergement.statut == statut)

        return await self.db.fetch_all(query)

    async def get_by_id_for_user(self, demande_id: UUID, demandeur_id: UUID):
        query = f"""
            SELECT * FROM {self.schema}.demande_hebergement
            WHERE id = :demande_id AND demandeur_id = :demandeur_id
        """
        return await self.db.fetch_one(query, values={"demande_id": demande_id, "demandeur_id": demandeur_id})

    # Utilisé par le traitement administratif (pas par le demandeur)
    async def get_by_id(self, demande_id: UUID):
        query = f"""
            SELECT * FROM {self.schema}.demande_hebergement
            WHERE id = :demande_id
        """
        return await self.db.fetch_one(query, values={"demande_id": demande_id})

    async def update_demande(self, demande_id: UUID, data: dict):
        # Mise à jour administrative ou utilisateur selon appel
        allowed_fields = {
            "motif", "date_arrivee", "date_depart", "justificatif_url",
            "statut", "motif_refus", "prise_en_charge_validee",
            "code_ligne_budgetaire", "hebergement_id"
        }
        update_data = {k: v for k, v in data.items() if k in allowed_fields}

        if not update_data:
            return None

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = f"""
            UPDATE {self.schema}.demande_hebergement
            SET {set_clause}
            WHERE id = :demande_id
            RETURNING *
        """
        values = {"demande_id": demande_id, **update_data}
        return await self.db.fetch_one(query, values=values)

    async def annuler_demande(self, demande_id: UUID):
        query = f"""
            UPDATE {self.schema}.demande_hebergement
            SET statut = 'ANNULEE'
            WHERE id = :demande_id AND statut = 'EN_ATTENTE'
            RETURNING *
        """
        return await self.db.fetch_one(query, values={"demande_id": demande_id})
    
    async def get_demandes_en_attente(self):
        query = f"""
            SELECT * FROM {POSTGRES_SCHEMA}.demande_hebergement
            WHERE statut = 'EN_ATTENTE'
            ORDER BY date_soumission DESC
        """
        return await self.db.fetch_all(query)