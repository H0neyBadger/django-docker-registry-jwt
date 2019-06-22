#!/bin/bash

set -euxo pipefail

podname=django-docker-registry-jwt_pod

# build container
podman build -t docker.io/django-docker-registry-jwt:latest .

podman pod rm -f "${podname}" && echo "done"
podman pod create --name "${podname}" \
  --publish "8443:8443" \
  --publish "5000:5000/tcp" 
 
podman rm -f django-docker-registry-jwt && echo "done"
podman run \
  --pod "${podname}" \
  --hostname django-docker-registry-jwt \
  --name django-docker-registry-jwt \
  --env POSTGRES_SERVICE_HOST=localhost \
  --env GUNICORN_KEYFILE=/app/pki/private/django.key \
  --env GUNICORN_CERT=/app/pki/issued/django.crt \
  --volume $(pwd)/settings.py:/etc/django/settings.py:ro \
  --volume $(pwd)/pki/private/django.key:/app/pki/private/django.key:ro \
  --volume $(pwd)/pki/issued/django.crt:/app/pki/issued/django.crt:ro \
  --volume $(pwd)/pki/private/token.key:/app/pki/private/token.key:ro \
  --volume $(pwd)/pki/issued/token.crt:/app/pki/issued/token.crt:ro \
  -d docker.io/django-docker-registry-jwt

podman rm -f postgres && echo "done"
podman run \
  --hostname postgres \
  --name postgres \
  --env POSTGRES_USER='postgres' \
  --env POSTGRES_DB='postgres' \
  -d docker.io/postgres

podman rm -f registry && echo "done"
podman run \
  --pod "${podname}" \
  --name registry \
  --env REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
  --env REGISTRY_AUTH=token \
  --env REGISTRY_AUTH_TOKEN_REALM=https://localhost:8443/docker-token-auth/ \
  --env REGISTRY_AUTH_TOKEN_SERVICE="127.0.0.1:5000" \
  --env REGISTRY_AUTH_TOKEN_ISSUER='127.0.0.1' \
  --env REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/pki/ca_bundle.crt \
  --volume $(pwd)/pki/ca_bundle.crt:/pki/ca_bundle.crt:ro \
  -d docker.io/registry

#podman exec -it django-docker-registry-jwt /usr/bin/entrypoint.sh python3 manage.py createsuperuser

