from pydantic import Field
from store.schemas.base import BaseSchemaMixin


class ProductIn(BaseSchemaMixin):
    name: str = Field(..., description="Product Name")
    quantity: int = Field(..., description="Product Quantity")
    price: float = Field(..., description="Product Price")
    status: bool = Field(..., description="Product Status")
