import os
from logging.config import fileConfig
from app.models import metadata
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Chargement des variables d'environnement (.env)
load_dotenv()

# Config générale Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import des modèles (schéma hebergement)
from app.models import (
    demande_hebergement,
    hebergement,
    ligne_budgetaire,
    invite,
    reservation
)

# Ciblage des metadata à exposer à Alembic
target_metadata = metadata

# Chargement dynamique des paramètres de connexion
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "hebergement")
DATABASE_URL = os.getenv("DATABASE_URL")

# Filtrage strict du schéma pour éviter les objets d'autres microservices
def include_object(obj, name, type_, reflected, compare_to):
    # On cible uniquement les tables du bon schéma
    if type_ == "table":
        return getattr(obj, "schema", None) == POSTGRES_SCHEMA
    # On laisse les autres objets (indexes, enums, ...) passer
    return True

# Mode OFFLINE (pas de connexion active)
def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=POSTGRES_SCHEMA,
        include_schemas=True,
        include_object=include_object,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Mode ONLINE (connexion active)
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=POSTGRES_SCHEMA,
            include_schemas=True,
            include_object=include_object,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

# Lancement selon le mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
