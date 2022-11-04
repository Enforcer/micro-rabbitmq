import logging

import requests
from opentelemetry.sdk.trace import Tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

import mqlib
from registry.order_placed_pydantic import OrderPlaced
from warehouse import db, legacy, queues, tracing

logging.basicConfig(level=logging.INFO)


class Consumer:
    def __init__(self, tracer: Tracer) -> None:
        self._tracer = tracer

    def consume(self, body: dict, message: mqlib.Message) -> None:
        message.ack()
        logging.info(
            "Received message: %r with headers %r and delivery info %r",
            body,
            message.headers,
            message.delivery_info,
        )
        propagator = TraceContextTextMapPropagator()
        context = propagator.extract(carrier=message.headers)
        with self._tracer.start_as_current_span(
            name="warehouse/consumer", context=context  # we pass context
        ):
            order_placed = OrderPlaced(**body)
            legacy.reserve_stock(product_id=order_placed.product_id)

            sizes = legacy.get_product_sizes(order_placed.product_id)
            requests.post(
                "http://shipping:8200/labels",
                json={
                    "weight": sizes.weight,
                    "width": sizes.width,
                    "length": sizes.length,
                    "height": sizes.height,
                },
            )


def setup() -> Tracer:
    queues.setup_queues()
    db.setup_database()
    tracer = tracing.setup("warehouse")
    return tracer


def main() -> None:
    tracer = setup()
    consumer = Consumer(tracer)
    mqlib.consume(consumer.consume, queues.order_placed)


if __name__ == "__main__":
    main()
