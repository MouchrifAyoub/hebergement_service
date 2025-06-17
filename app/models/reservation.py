import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.settings import POSTGRES_SCHEMA
from app.models.base import Base

class Reservation(Base):
    __tablename__ = "reservation"
    __table_args__ = {"schema": "hebergement"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invite_id = Column(UUID(as_uuid=True), ForeignKey(f"{POSTGRES_SCHEMA}.invite.id"), nullable=False)
    date_arrivee = Column(Date, nullable=False)
    date_depart = Column(Date, nullable=False)
    statut = Column(String, nullable=False, default="CONFIRMEE")  # CONFIRMEE, ANNULEE
