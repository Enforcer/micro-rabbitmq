from typing import Protocol

from kombu import Connection, Exchange, Queue
from kombu.connection import ConnectionPool
from kombu.pools import connections
from pydantic import AmqpDsn, BaseSettings, Field

__all__ = ["publish", "declare", "consume", "Message"]


class BrokerSettings(BaseSettings):
    BROKER_URL: AmqpDsn = Field(default="amqp://guest:guest@rabbitmq//")


class PoolFactory:
    _pool: ConnectionPool | None = None

    @classmethod
    def get(cls) -> ConnectionPool:
        if cls._pool is None:
            connection = Connection(
                BrokerSettings().BROKER_URL, transport_options={"confirm_publish": True}
            )
            cls._pool = connections[connection]
        return cls._pool


ANONYMOUS_EXCHANGE = ""


def publish(queue_name_or_queue: str | Queue, message: dict, headers: dict | None) -> None:
    headers = headers or {}
    if isinstance(queue_name_or_queue, Queue):
        queue = queue_name_or_queue.name
    else:
        queue = queue_name_or_queue

    with PoolFactory.get().acquire(block=True) as conn:
        producer = conn.Producer(serializer="json")
        producer.publish(
            message,
            exchange=ANONYMOUS_EXCHANGE,
            routing_key=queue,
            headers=headers,
            # retry=True,
            # retry_policy={
            #     'interval_start': 0,  # First retry immediately,
            #     'interval_step': 2,  # then increase by 2s for every retry.
            #     'interval_max': 30,  # but don't exceed 30s between retries.
            #     'max_retries': 30,  # give up after 30 tries.
            # },
        )


def declare(queue_or_exchange: Exchange | Queue) -> None:
    with PoolFactory.get().acquire(block=True) as conn:
        queue_or_exchange(conn).declare()


class Message(Protocol):
    headers: dict[str, str]
    properties: dict[str, str]
    delivery_info: dict[str, str]

    def ack(self) -> None:
        ...

    def reject(self) -> None:
        ...


class ConsumptionCallback(Protocol):
    def __call__(self, body: dict, message: Message) -> None:
        ...


def consume(callback: ConsumptionCallback, *queues: Queue) -> None:
    with PoolFactory.get().acquire(block=True) as conn:
        with conn.Consumer(list(queues), callbacks=[callback]):
            while True:
                try:
                    conn.drain_events()
                except KeyboardInterrupt:
                    return
