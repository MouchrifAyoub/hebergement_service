import uuid
from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.config.settings import POSTGRES_SCHEMA
from app.models.base import Base

class LigneBudgetaire(Base):
    __tablename__ = "ligne_budgetaire"
    __table_args__ = {"schema": POSTGRES_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    montant_disponible = Column(Numeric, nullable=False)
