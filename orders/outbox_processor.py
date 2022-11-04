from orders import db, queues


def main() -> None:
    _setup()

    while True:
        break  # TODO: implement outbox processor
        single_run()


def single_run() -> None:
    with db.Session() as session:
        session.execute("SELECT 1")


def _setup() -> None:
    db.setup_database()
    queues.setup_queues()


if __name__ == "__main__":
    main()
