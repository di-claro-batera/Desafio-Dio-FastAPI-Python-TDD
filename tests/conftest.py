import asyncio
import pytest
from store.db.mongo import db_client


@pytest.fixture(scope="session")
def event_loop():
    """Cria uma instância do event loop para a sessão de testes."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def mongo_client():
    """Fixture para obter o cliente MongoDB."""
    client = db_client.get()
    yield client
    await client.close()  # Note o await aqui


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    """Limpa todas as coleções antes de cada teste."""
    db = mongo_client.get_database()
    collections = await db.list_collection_names()

    for collection_name in collections:
        if not collection_name.startswith("system"):
            await db[collection_name].delete_many({})
