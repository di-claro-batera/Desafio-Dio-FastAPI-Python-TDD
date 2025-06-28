import asyncio
from uuid import UUID
import uuid
import pytest
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import products_data
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
from store.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client():
    return db_client.get()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue
        await mongo_client.get_database().get_collection(collection_name).delete_many(
            {}
        )
    yield


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> uuid.UUID:
    return UUID("ddf4fbf1-10cc-4eda-8af3-8086f9063dc8")


@pytest.fixture
def product_in(product_data, product_id):
    return ProductIn(**product_data, id=product_id)


@pytest.fixture
def product_data():
    return {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8500",
        "status": True,
    }


@pytest.fixture
def product_up(product_data, product_id):
    return ProductUpdate(**product_data, id=product_id)


@pytest.fixture
async def product_inserted(product_in):
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product) for product in products_in]
