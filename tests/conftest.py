import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app

# Configuration d'environnement forcée pour les tests
os.environ["DATABASE_URL"] = "postgresql://postgres:Postgres2025!@localhost:5432/fms"
os.environ["POSTGRES_SCHEMA"] = "hebergement"

@pytest_asyncio.fixture
async def async_client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            yield client
