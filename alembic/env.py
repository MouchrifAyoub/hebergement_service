import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 🔁 Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# 📜 Config Alembic
config = context.config

# 📊 Logging Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🎯 Metadata ciblée (pas encore définie si on n'a pas encore de models)
target_metadata = None

# 🏷️ Chargement des infos de connexion
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")
DATABASE_URL = os.getenv("DATABASE_URL")

def run_migrations_offline() -> None:
    """Migrations en mode offline (sans connexion active)"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=POSTGRES_SCHEMA,
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Migrations en mode online (avec vraie connexion)"""

    # injection dans la section sqlalchemy.url du fichier ini
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

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
        )

        with context.begin_transaction():
            context.run_migrations()


# ⚙️ Lancer le bon mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
