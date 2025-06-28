from bson import Decimal128
from decimal import Decimal
from uuid import UUID
from datetime import datetime, timezone

from store.models.base import CreateBaseModel
from store.schemas.product import ProductIn


class ProductModel(ProductIn, CreateBaseModel):
    def mongo_dict(self) -> dict:
        data = self.model_dump()
        data["_id"] = str(data.pop("id"))

        if "price" in data and isinstance(data["price"], Decimal):
            data["price"] = Decimal128(str(data["price"]))

        return data

    @classmethod
    def from_mongo(cls, data: dict):
        data = data.copy()

        if "_id" in data:
            data["id"] = UUID(data.pop("_id"))

        for key, value in data.items():
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))

        if "created_at" not in data:
            data["created_at"] = datetime.now(timezone.utc)
        if "updated_at" not in data:
            data["updated_at"] = datetime.now(timezone.utc)

        return cls(**data)
