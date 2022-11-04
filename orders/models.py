from sqlalchemy import Column, Integer, Numeric, String
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
    queue = Column(String(255), nullable=False)
    data = Column(JSON(), nullable=False)
    headers = Column(JSON(), nullable=False)
