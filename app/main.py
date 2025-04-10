from fastapi import FastAPI
from app.api import hebergement_controller
from app.config.database import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Inclusion routes
app.include_router(hebergement_controller.router, prefix="/hebergement", tags=["Hébergement"])
