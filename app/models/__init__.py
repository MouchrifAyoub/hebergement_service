from .base import Base
metadata = Base.metadata  # ✅ Ceci est ce que Alembic va utiliser

from app.models.demande_hebergement import DemandeHebergement
from app.models.hebergement import Hebergement
from app.models.invite import Invite
from app.models.reservation import Reservation
from app.models.ligne_budgetaire import LigneBudgetaire
