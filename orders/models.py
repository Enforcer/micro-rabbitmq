from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.dialects.postgresql import JSON

from orders.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    quantity = Column(Integer(), nullable=False)
    price = Column(Numeric(), nullable=False)


class OutboxEntry(Base):
    __tablename__ = "outbox_entries"

    id = Column(Integer(), primary_key=True)
    data = Column(JSON(), nullable=False)
