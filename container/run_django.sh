#!/bin/bash

/usr/bin/wait_for_connection.py POSTGRES_SERVICE_HOST ${POSTGRES_SERVICE_PORT:-5432}

django-admin collectstatic --noinput

django-admin makemigrations
django-admin migrate --noinput

gunicorn --bind '0.0.0.0:8443' wsgi \
    --keyfile=${GUNICORN_KEYFILE} \
    --certfile=${GUNICORN_CERT} \
    --access-logfile -
