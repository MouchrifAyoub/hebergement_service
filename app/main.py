# from fastapi import FastAPI
# from app.api import hebergement_controller
# from app.config.database import database

# app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

# # Inclusion routes
# app.include_router(hebergement_controller.router, prefix="/hebergement", tags=["Hébergement"])



import sys
sys.path.append('../common')

from fastapi import FastAPI
from app.api import hebergement_controller
from app.config.database import database

# Common imports
from common.retry import example_retry
from common.logging_config import setup_logging
from common.config import settings
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Setup logging
    setup_logging()

    # Log config value (just as a test)
    app.logger = app.logger if hasattr(app, 'logger') else None
    print(f"Loaded config from Dynaconf: {settings.as_dict()}")

    # Call retry test (can comment out later in prod)
    try:
        await example_retry()
    except Exception as e:
        print(f"Retry test ended with exception: {e}")

    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Inclusion routes
app.include_router(hebergement_controller.router, prefix="/hebergement", tags=["Hébergement"])
