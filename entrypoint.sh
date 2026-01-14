#!/bin/sh
set -e

python manage.py migrate --noinput

export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-adminadmin}"

python manage.py createsuperuser --noinput || true

python manage.py runserver 0.0.0.0:${PORT:-8000} --noreload
