import csv
from typing import List, Optional
from uuid import UUID
from fastapi import UploadFile
from app.repositories.demande_hebergement_repository import DemandeHebergementRepository
from app.repositories.invite_repository import InviteRepository
from app.schemas.invite import InviteCreate, InviteOut

class InviteService:
    def __init__(self, repository: InviteRepository, demande_repo: Optional[DemandeHebergementRepository] = None):
        self.repository = repository
        self.demande_repo = demande_repo

    async def add_invite(self, demande_id: UUID, invite_data: InviteCreate) -> InviteOut:
        if self.demande_repo:
            demande = await self.demande_repo.get_by_id(demande_id)
            if not demande:
                raise ValueError("Demande d’hébergement associée introuvable.")
            
        if invite_data.date_arrivee >= invite_data.date_depart:
            raise ValueError("La date d’arrivée doit être antérieure à la date de départ.")

        is_dispo = await self.check_disponibilite(
            invite_data.type_hebergement,
            invite_data.date_arrivee,
            invite_data.date_depart
        )
        if not is_dispo:
            raise ValueError(f"{invite_data.type_hebergement} non disponible pour les dates sélectionnées.")
        
        invite = await self.repository.create(
            demande_id,
            invite_data.nom,
            invite_data.prenom,
            invite_data.fonction,
            invite_data.date_arrivee,
            invite_data.date_depart,
            invite_data.email,
            invite_data.telephone,
            invite_data.type_hebergement
        )
        return InviteOut.model_validate(invite)


    async def get_invites_for_demande(self, demande_id: UUID) -> List[InviteOut]:
        invites = await self.repository.get_by_demande_id(demande_id)
        return [InviteOut.model_validate(i) for i in invites]

    async def import_from_csv(self, demande_id: UUID, csv_file: UploadFile):
        content = await csv_file.read()
        decoded = content.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)

        invites_added = []
        for row in reader:
            invite = await self.repository.create(
                demande_id,
                row['nom'],
                row['prenom'],
                row.get('fonction', ''),
                row['date_arrivee'],
                row['date_depart'],
                row.get('email', ''),
                row.get('telephone', ''),
                row.get('type_hebergement', '')
            )
            invites_added.append(invite)

        return invites_added
    
    async def check_disponibilite(self, type_hebergement: str, date_arrivee, date_depart) -> bool:
        return await self.repository.check_disponibilite(type_hebergement, date_arrivee, date_depart)
