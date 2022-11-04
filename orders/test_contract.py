from pathlib import Path
from typing import Iterator

import pytest as pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

import mqlib.testing
import registry.order_placed_event_pb2
import registry.order_placed_pydantic
from orders import db, outbox_processor, queues
from orders.api import app


def test_order_placed_event_message_can_be_decoded_using_shared_schema(
    client: TestClient,
) -> None:
    mqlib.testing.purge(queues.order_placed)

    response = client.post(
        "/orders", json={"product_id": 1, "price": 7.99, "quantity": 1}
    )
    assert response.status_code == 202
    outbox_processor.single_run()

    message = mqlib.testing.next_message(queues.order_placed)
    # With protobuf
    protobuf_message = registry.order_placed_event_pb2.OrderPlaced(**message)
    assert protobuf_message.id > 0  # not default
    assert protobuf_message.product_id == 1
    assert protobuf_message.price == "7.99"
    assert protobuf_message.quantity == 1
    # With Pydantic
    pyd_model = registry.order_placed_pydantic.OrderPlaced(**message)
    assert pyd_model == registry.order_placed_pydantic.OrderPlaced(
        id=message["id"],
        product_id=1,
        price="7.99",
        quantity=1,
    )


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reconfigure_app_for_testing(tmp_path: Path) -> None:
    test_db_path = str(tmp_path / "test.sqlite")
    test_engine = create_engine(f"sqlite:///{test_db_path}", future=True)
    db.Session.configure(bind=test_engine)
