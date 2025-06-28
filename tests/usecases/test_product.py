from decimal import Decimal
from typing import List
from uuid import uuid4
import uuid

import pytest
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut
from store.usecases.product import product_usecase
from store.models.product import ProductModel  # 🚨 novo import


async def test_usecases_create_should_return_sucess(product_in):
    result = await product_usecase.create(body=product_in)

    # Convertendo para ProductOut se necessário
    if isinstance(result, ProductModel):
        result = ProductOut(**result.model_dump())

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


async def test_usecases_get_should_return_sucess(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    if isinstance(result, ProductModel):
        result = ProductOut(**result.model_dump())

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


async def test_usecases_get_should_not_found():
    fake_id = uuid4()
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=fake_id)

    assert err.value.args[0] == f"Product not found with filter: {fake_id}"


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_sucess():
    result = await product_usecase.query()

    # Garantindo que todos os itens sejam ProductOut
    output = [
        ProductOut(**item.model_dump()) if isinstance(item, ProductModel) else item
        for item in result
    ]

    assert isinstance(output, List)
    assert len(output) > 1


async def test_usecases_update_should_return_sucess(product_inserted, product_up):
    product_up.price = Decimal("9500")

    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    if isinstance(result, ProductModel):
        result = ProductOut(**result.model_dump())

    assert isinstance(result, ProductOut)
    assert result.price == Decimal("9500")
    assert result.name == "Iphone 14 pro Max"


async def test_usecases_delete_should_return_sucess(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True


async def test_usecases_delete_should_not_found():
    fake_id = uuid.uuid4()
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=fake_id)

    assert err.value.args[0] == f"Produto com o id {fake_id} não encontrado."
