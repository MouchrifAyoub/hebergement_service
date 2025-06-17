import enum

class StatutDemande(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VALIDEE = "VALIDEE"
    REFUSEE = "REFUSEE"
    ANNULEE = "ANNULEE"
    ARCHIVEE = "ARCHIVEE"
