import uuid
from sqlalchemy import Column, String, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.config.settings import POSTGRES_SCHEMA
from app.enums.type_hebergement import TypeHebergement
from app.models.base import Base

class Invite(Base):
    __tablename__ = "invite"
    __table_args__ = {"schema": "hebergement"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    demande_id = Column(UUID(as_uuid=True), ForeignKey(f"{POSTGRES_SCHEMA}.demande_hebergement.id"), nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    fonction = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    type_hebergement = Column(Enum(TypeHebergement), nullable=False)
    date_arrivee = Column(Date, nullable=False)
    date_depart = Column(Date, nullable=False)
