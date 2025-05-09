from app.repositories.ligne_budgetaire_repository import LigneBudgetaireRepository
from app.schemas.ligne_budgetaire import LigneBudgetaireCreate, LigneBudgetaireOut

class LigneBudgetaireService:
    def __init__(self, repository: LigneBudgetaireRepository):
        self.repository = repository

    async def create_ligne_budgetaire(self, data: LigneBudgetaireCreate) -> LigneBudgetaireOut:
        ligne = await self.repository.create(
            data.code,
            data.description,
            data.montant_disponible
        )
        return LigneBudgetaireOut(**ligne.__dict__)

    async def get_ligne_by_code(self, code: str) -> LigneBudgetaireOut:
        ligne = await self.repository.get_by_code(code)
        if ligne is None:
            raise ValueError("Ligne budgétaire non trouvée")
        return LigneBudgetaireOut(**ligne.__dict__)

    async def update_montant(self, code: str, new_montant) -> LigneBudgetaireOut:
        ligne = await self.repository.update_montant(code, new_montant)
        if ligne is None:
            raise ValueError("Échec de mise à jour du montant")
        return LigneBudgetaireOut(**ligne.__dict__)
