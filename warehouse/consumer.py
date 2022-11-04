import logging

import requests

import mqlib
from warehouse import db, legacy, queues

logging.basicConfig(level=logging.INFO)


def consume(body: dict, message: mqlib.Message) -> None:
    message.ack()
    logging.info(
        "Received message: %r with headers %r and delivery info %r",
        body,
        message.headers,
        message.delivery_info,
    )
    legacy.reserve_stock(product_id=body["product_id"])

    sizes = legacy.get_product_sizes(body["product_id"])
    requests.post(
        "http://shipping:8200/labels",
        json={
            "weight": sizes.weight,
            "width": sizes.width,
            "length": sizes.length,
            "height": sizes.height,
        },
    )


def setup():
    queues.setup_queues()
    db.setup_database()


def main() -> None:
    setup()
    mqlib.consume(consume, queues.order_placed)


if __name__ == "__main__":
    main()
