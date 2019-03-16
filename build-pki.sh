#!/bin/bash

curl -L -O https://storage.googleapis.com/kubernetes-release/easy-rsa/easy-rsa.tar.gz
tar xzf easy-rsa.tar.gz

set -eux

export EASYRSA_PKI="$(pwd)/pki"

pushd "./easy-rsa-master/easyrsa3/"
# MASTER_IP="django-docker-registry-jwt"
MASTER_IP="127.0.0.1"


./easyrsa init-pki
./easyrsa --batch "--req-cn=${MASTER_IP}@`date +%s`" build-ca nopass

./easyrsa --subject-alt-name="IP:${MASTER_IP}" build-server-full django nopass
./easyrsa --subject-alt-name="IP:${MASTER_IP}" build-server-full registry nopass

# set elliptic curve for docker token
export EASYRSA_ALGO=ec
export EASYRSA_CURVE="P-256"

./easyrsa --subject-alt-name="IP:${MASTER_IP}" build-server-full token nopass
popd

# create bundle from ca + pk
cat ./pki/ca.crt \
    ./pki/issued/token.crt \
    > ./pki/ca_bundle.crt


# set selinux context
sudo chcon -t container_file_t \
    ./settings_prd.py \
    ./pki/ca_bundle.crt \
    ./pki/private/django.key \
    ./pki/issued/django.crt \
    ./pki/private/registry.key \
    ./pki/issued/registry.crt \
    ./pki/private/token.key \
    ./pki/issued/token.crt

