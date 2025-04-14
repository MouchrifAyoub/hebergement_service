import uuid
from datetime import date, datetime
from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.settings import POSTGRES_SCHEMA
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class StatutDemande(enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VALIDEE = "VALIDEE"
    REFUSEE = "REFUSEE"
    ANNULEE = "ANNULEE"
    ARCHIVEE = "ARCHIVEE"

class DemandeHebergement(Base):
    __tablename__ = "demande_hebergement"
    __table_args__ = {"schema": POSTGRES_SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_soumission = Column(DateTime, default=datetime.utcnow)
    date_arrivee = Column(Date, nullable=False)
    date_depart = Column(Date, nullable=False)
    motif = Column(String, nullable=False)
    statut = Column(Enum(StatutDemande), default=StatutDemande.EN_ATTENTE)
    justificatif_url = Column(String, nullable=True)
    code_ligne_budgetaire = Column(String, nullable=True)
    demandeur_id = Column(UUID(as_uuid=True), nullable=False)
