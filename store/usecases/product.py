from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from typing import List, Optional

from bson import Decimal128
import pymongo
from store.core.exceptions import InsertException, NotFoundException
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product_model = ProductModel(**body.model_dump())
            await self.collection.insert_one(product_model.mongo_dict())
            return ProductOut(**product_model.model_dump())
        except Exception as e:
            raise InsertException("Erro ao inserir o produto.") from e

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"_id": str(id)})
        if not result:
            raise NotFoundException(f"Product not found with filter: {id}")
        return ProductModel.from_mongo(result)

    async def query(self) -> List[ProductOut]:
        return [ProductModel.from_mongo(doc) async for doc in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        data = body.model_dump(exclude_none=True)

        if "price" in data and isinstance(data["price"], Decimal):
            data["price"] = Decimal128(str(data["price"]))

        data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            filter={"_id": str(id)},
            update={"$set": data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(f"Produto com o id {id} não encontrado.")

        return ProductModel.from_mongo(result)

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"_id": str(id)})

        if result.deleted_count == 0:
            raise NotFoundException(f"Produto com o id {id} não encontrado.")

        return True

    async def filter_by_price(
        self, min_price: Optional[Decimal], max_price: Optional[Decimal]
    ) -> List[ProductOut]:
        query = {}

        price_query = {}
        if min_price is not None:
            price_query["$gte"] = Decimal128(str(min_price))
        if max_price is not None:
            price_query["$lte"] = Decimal128(str(max_price))
        if price_query:
            query["price"] = price_query

        cursor = self.collection.find(query)
        return [ProductModel.from_mongo(doc) async for doc in cursor]


product_usecase = ProductUsecase()
