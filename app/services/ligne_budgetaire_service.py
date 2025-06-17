from app.repositories.ligne_budgetaire_repository import LigneBudgetaireRepository
from app.schemas.ligne_budgetaire import LigneBudgetaireCreate, LigneBudgetaireOut

class LigneBudgetaireService:
    def __init__(self, repository: LigneBudgetaireRepository):
        self.repository = repository

    async def create_ligne_budgetaire(self, data: LigneBudgetaireCreate) -> LigneBudgetaireOut:
        existing = await self.repository.get_by_code(data.code)
        if existing:
            raise ValueError("Une ligne budgétaire avec ce code existe déjà")
        if data.montant_disponible <= 0:
            raise ValueError("Le montant doit être strictement supérieur à 0")
        ligne = await self.repository.create(
            data.code,
            data.description,
            data.montant_disponible
        )
        return LigneBudgetaireOut.model_validate(ligne)

    async def get_ligne_by_code(self, code: str) -> LigneBudgetaireOut:
        ligne = await self.repository.get_by_code(code)
        if ligne is None:
            raise ValueError("Ligne budgétaire non trouvée")
        return LigneBudgetaireOut.model_validate(ligne)

    async def update_montant(self, code: str, new_montant) -> LigneBudgetaireOut:
        ligne = await self.repository.update_montant(code, new_montant)
        if ligne is None:
            raise ValueError("Échec de mise à jour du montant")
        return LigneBudgetaireOut.model_validate(ligne)
    
    async def get_all(self):
        lignes = await self.repository.get_all()
        return [LigneBudgetaireOut.model_validate(ligne) for ligne in lignes]
