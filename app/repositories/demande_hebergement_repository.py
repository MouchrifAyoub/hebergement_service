from app.models.demande_hebergement import DemandeHebergement, StatutDemande
from app.schemas.demande_hebergement import DemandeHebergementCreate
from sqlalchemy import select, and_, insert
from databases import Database
from uuid import UUID
from datetime import datetime
from typing import Optional, List
import uuid


class DemandeHebergementRepository:
    def __init__(self, db: Database):
        self.db = db

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
        print("→ Vérification d'une demande existante...")
        result = await self.db.fetch_one(query)
        print("→ Résultat trouvé :", result)
        return result is not None

    async def get_all_by_demandeur_id(self, demandeur_id: UUID, statut: Optional[str] = None) -> List[DemandeHebergement]:
        query = select(DemandeHebergement).where(DemandeHebergement.demandeur_id == demandeur_id)

        if statut:
            query = query.where(DemandeHebergement.statut == statut)

        return await self.db.fetch_all(query)
