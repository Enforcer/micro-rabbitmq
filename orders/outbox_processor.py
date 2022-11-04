from datetime import timedelta
from time import sleep

import mqlib
from orders import db, outbox, queues

INTERVAL = timedelta(seconds=5)
BATCH_SIZE = 100


def main() -> None:
    _setup()

    while True:
        single_run()
        sleep(INTERVAL.total_seconds())


def single_run() -> None:
    with db.Session() as session:
        with outbox.batch(session, size=BATCH_SIZE) as batch:
            for queue_name, message, headers in batch:
                mqlib.publish(
                    queue_name_or_queue=queue_name, message=message, headers=headers
                )
        session.commit()


def _setup() -> None:
    db.setup_database()
    queues.setup_queues()


if __name__ == "__main__":
    main()
