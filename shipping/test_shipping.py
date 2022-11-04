from typing import Iterator

import pytest
from fastapi.testclient import TestClient

from shipping.api import app


def test_product_gets_estimated_price_and_label(client: TestClient) -> None:
    response = client.post(
        "/labels",
        json={
            "weight": 1,
            "width": 20,
            "height": 5,
            "length": 30,
        },
    )
    assert response.status_code == 200

    label_id = response.json()["id"]
    get_response = client.get(f"/labels/{label_id}")
    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": label_id,
        "weight": 1,
        "width": 20,
        "height": 5,
        "length": 30,
        "price": 12.99,
    }


@pytest.fixture()
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
