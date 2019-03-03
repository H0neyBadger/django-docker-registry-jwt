docker run --rm -p 5000:5000 \
-e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
-e REGISTRY_AUTH=token \
-e REGISTRY_AUTH_TOKEN_REALM=http://127.0.0.1:8000/docker-token-auth/ \
-e REGISTRY_AUTH_TOKEN_SERVICE="127.0.0.1:8000" \
-e REGISTRY_AUTH_TOKEN_ISSUER='127.0.0.1' \
-e REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/ssl/ca.crt \
-v $(pwd)/easy-rsa-master/easyrsa3/pki/ca_bundle.crt:/ssl/ca.crt:ro \
--name registry registry:2
