# Hébergement Service – SHCC Web Portal

Ce microservice fait partie de la plateforme web centralisée de digitalisation des processus internes de la FMS – UM6P. Il est dédié à la **gestion des demandes d'hébergement**, avec une architecture orientée microservices.

## 📌 Fonctionnalités couvertes

- Soumission des demandes d’hébergement (internes ou invités)
- Modification / annulation d’une demande
- Consultation de l’historique des demandes
- Traitement des demandes par le responsable (validation, refus)
- Affectation des lignes budgétaires
- Création des réservations pour les invités

## 🏗️ Architecture

- **Framework** : FastAPI (Python)
- **Database** : PostgreSQL (schéma dédié : `hebergement`)
- **ORM** : Aucun – Requêtes SQL manuelles via `asyncpg` + `databases`
- **Migrations** : Alembic (multi-schema support)
- **Environnement** : Gestion via `poetry` et `.env`
- **API REST**

## 📂 Structure du projet

```
HEBERGEMENT_SERVICE/
├── alembic/              # Scripts de migration Alembic
│   ├── versions/         # Migrations versionnées
│   └── env.py            # Configuration des migrations (multi-schema)
├── app/
│   ├── api/              # Définition des routes FastAPI
│   ├── config/           # Fichiers de configuration (.env, DB, settings)
│   ├── models/           # Représentations des entités (sans ORM)
│   ├── repositories/     # Requêtes SQL vers la base
│   ├── schemas/          # Pydantic schemas (requêtes / réponses)
│   ├── services/         # Logique métier (validation, règles, etc.)
│   ├── utils/            # Fonctions utilitaires
│   └── main.py           # Entrée principale FastAPI
├── tests/                # Tests unitaires (à venir)
├── .env                  # Variables d'environnement locales
├── alembic.ini           # Configuration Alembic
├── poetry.lock / pyproject.toml
└── README.md             # Ce fichier
```

## ⚙️ Configuration requise

Créer un fichier `.env` à la racine avec le contenu suivant :

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/ma_basedonnee
POSTGRES_SCHEMA=hebergement
APP_ENV=dev
```

## ▶️ Lancer le service

```bash
# Installer les dépendances
poetry install

# Activer l'environnement virtuel
poetry shell

# Lancer le serveur FastAPI
uvicorn app.main:app --reload
```

## 🔄 Migrations Alembic

```bash
# Générer une nouvelle migration
alembic revision -m "Nom de la migration" --schema=hebergement

# Appliquer les migrations
alembic upgrade head
```

## 🧪 Tests

```bash
# (à venir)
```

