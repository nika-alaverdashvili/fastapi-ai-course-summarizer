#!/bin/sh

# PostgresSQL check
echo "Waiting for PostgresSQL to start..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "PostgresSQL is unavailable - sleeping..."
  sleep 1
done
echo "PostgresSQL is up!"


# Redis check
if command -v redis-cli > /dev/null; then
  echo "Waiting for Redis to start..."
  until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping | grep -q PONG; do
    echo "Redis is unavailable - sleeping..."
    sleep 1
  done
  echo "Redis is up!"
else
  echo "redis-cli not found, skipping Redis check."
fi

exec "$@"
