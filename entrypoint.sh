#!/bin/sh

echo "Waiting for PostgresSQL to start..."

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "PostgresSQL is unavailable - sleeping..."
  sleep 1
done

echo "PostgresSQL is up!"
exec "$@"
