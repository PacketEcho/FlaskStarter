#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT";
do
  sleep 0.1
done

echo "PostgreSQL started"

echo '################# dropping DB #################'
python manage.py drop_db
echo '################# creating DB #################'
python manage.py create_db

gunicorn -b 0.0.0.0:5000 autoapp:app