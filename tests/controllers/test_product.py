from typing import List

import pytest
from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_sucess(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content["id"]
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8500",
        "status": True,
    }


async def test_controller_get_should_return_sucess(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8500",
        "status": True,
    }


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}ddf4fbf1-10cc-4eda-8af3-8086f9063dc8")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: ddf4fbf1-10cc-4eda-8af3-8086f9063dc8"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_sucess(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_sucess(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "12000"}
    )

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "12000",
        "status": True,
    }


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}ddf4fbf1-10cc-4eda-8af3-8086f9063dc8"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"]
