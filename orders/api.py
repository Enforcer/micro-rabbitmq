from fastapi import Depends, FastAPI, Response
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

import mqlib
from orders import db, queues
from orders.models import Order


def get_session() -> Session:
    with db.Session() as session:
        yield session


class OrderDto(BaseModel):
    product_id: int
    price: float
    quantity: int

    @validator("price")
    def check_price(cls, price: float) -> float:
        if price < 0:
            raise ValueError("Price must be positive")
        return price

    @validator("quantity")
    def check_quantity(cls, quantity: int) -> int:
        if quantity < 0:
            raise ValueError("Quantity must be positive")
        return quantity


app = FastAPI()


@app.on_event("startup")
def initialize() -> None:
    db.setup_database()
    queues.setup_queues()


@app.post("/orders", status_code=202)
def order(dto: OrderDto, session: Session = Depends(get_session)) -> Response:
    order = Order(
        product_id=dto.product_id,
        price=dto.price,
        quantity=dto.quantity,
    )
    session.add(order)
    session.flush()

    mqlib.publish(
        queues.order_placed,
        {
            "id": order.id,
            "price": order.price,
            "quantity": order.quantity,
            "product_id": order.product_id,
        },
    )

    session.commit()
    return Response(status_code=202)
