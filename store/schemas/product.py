from decimal import Decimal
from typing import Optional
from pydantic import Field
from store.schemas.base import BaseSchemaMixin, OutMixin


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product Name")
    quantity: int = Field(..., description="Product Quantity")
    price: Decimal = Field(..., description="Product Price")
    status: bool = Field(..., description="Product Status")


class ProductIn(ProductBase, BaseSchemaMixin):
    pass


class ProductOut(OutMixin, ProductIn): ...


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product Quantity")
    price: Optional[Decimal] = Field(None, description="Product Price")
    status: Optional[bool] = Field(None, description="Product Status")


class ProductUpdateOut(ProductOut): ...
