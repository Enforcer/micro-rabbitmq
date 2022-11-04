# Communication in distributed systems with RabbitMQ

## Prerequisites
- docker (with docker compose)
- favourite IDE

## Setting up the project

### Build common image
```bash
docker compose build shell
```

### Start everything up
(code is autoreloaded)
```bash
docker compose up
```

### Resetting

In case you mande changes to DB schema (it's automatically created when each project starts) you may need to recreate containers.

```bash
<CTRL+C> (in running docker compose)
docker compose down -v
docker compose up
```

## Accessing services

Orders `http://localhost:8100/docs`

Shipping `http://localhost:8200/docs`

RabbitMQ `http://localhost:15672` (username: guest password: guest)

PostgreSQL: `docker exec -it micro-rabbitmq-db-1 psql -U guest`

Zipkin: `http://localhost:9411`
