docker run --rm -p 5000:5000 \
-e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
-e REGISTRY_AUTH=token \
-e REGISTRY_AUTH_TOKEN_REALM=http://127.0.0.1:8000/api-token-auth/ \
-e REGISTRY_AUTH_TOKEN_SERVICE="Docker registry" \
-e REGISTRY_AUTH_TOKEN_ISSUER="Auth Service" \
-e REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/ssl/ca.crt \
-v $(pwd)/easy-rsa-master/easyrsa3/pki/:/ssl:ro \
--name registry registry:2
