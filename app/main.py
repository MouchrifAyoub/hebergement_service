from fastapi import FastAPI
from app.api import (
    hebergement_controller,
    invite_controller,
    ligne_budgetaire_controller,
    reservation_controller
)
from app.config.database import database

# Common imports
from common.retry import example_retry
from common.logging_config import setup_logging
from common.config import settings
import asyncio

app = FastAPI(title="Hebergement Service")

@app.on_event("startup")
async def startup():
    # Setup logging
    setup_logging()

    # Log config value (just as a test)
    app.logger = app.logger if hasattr(app, 'logger') else None
    print(f"Loaded config from Dynaconf: {settings.as_dict()}")

    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Inclusion routes
app.include_router(hebergement_controller.router, prefix="/hebergement", tags=["Hébergement"])
app.include_router(invite_controller.router, prefix="/invites", tags=["Invités"])
app.include_router(ligne_budgetaire_controller.router, prefix="/hebergement", tags=["Ligne budgétaire"])
app.include_router(reservation_controller.router, prefix="/hebergement", tags=["Réservations invités"])