#!/bin/sh

echo "Esperando a que la base de datos esté lista..."
until pg_isready -h db -p 5432 -U postgres
do
  echo "Esperando a que la base de datos se inicie..."
  sleep 2
done
echo "Base de datos lista!"

exec /scripts/command-dev.sh