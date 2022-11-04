from kombu import Queue

import mqlib

order_placed = Queue("orders.events.order_placed", durable=True)


def setup_queues():
    mqlib.declare(order_placed)
