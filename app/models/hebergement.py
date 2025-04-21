import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.config.settings import POSTGRES_SCHEMA
from app.models.base import Base  # ✅ Base partagée

class Hebergement(Base):
    __tablename__ = "hebergement"
    __table_args__ = {"schema": POSTGRES_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, nullable=False)
    type = Column(String, nullable=False)  # Résidence, Hôtel, etc.
    disponible = Column(Boolean, default=True)
