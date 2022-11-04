from contextlib import contextmanager
from typing import Iterator, Tuple

from kombu import Queue
from sqlalchemy.orm import Session

from orders.models import OutboxEntry


def put(session: Session, message: dict, queue: Queue) -> None:
    entry = OutboxEntry(data=message, queue=queue.name)
    session.add(entry)


@contextmanager
def batch(session: Session, size: int) -> Iterator[Tuple[str, dict]]:
    entries: list[OutboxEntry] = (
        session.query(OutboxEntry)
        .order_by(OutboxEntry.id)  # we're sending 'oldest' entries first
        .with_for_update(skip_locked=True)  # this ensures safety with multiple workers
        .limit(size)  # we don't want to send the entire database at once
        .all()
    )
    yield ((entry.queue, entry.data) for entry in entries)
    # at the end, we remove entries so we don't send them again
    entries_ids = [entry.id for entry in entries]
    session.query(OutboxEntry).filter(OutboxEntry.id.in_(entries_ids)).delete(
        synchronize_session=False
    )
