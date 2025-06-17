import enum

class TypeHebergement(str, enum.Enum):
    HOTEL = "Hôtel"
    RESIDENCE = "Résidence"
    AUTRE = "Autre"