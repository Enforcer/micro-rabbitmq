from pydantic import BaseModel


class OrderPlaced(BaseModel):
    id: int
    product_id: int
    price: float
    quantity: float
