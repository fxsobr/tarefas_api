#!/bin/sh

echo "Aguardando Postgres..."

while ! nc -z tarefas-db 5432; do
  sleep 0.1
done

echo "PostgreSQL Inicializado"

python manage.py run -h 0.0.0.0