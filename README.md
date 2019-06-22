Django rest jwt for docker registry 
===================================

A simple (work in progress) rest api to handle docker registy v2 authorizations

Docs :
* https://docs.docker.com/registry/spec/auth/jwt/
* https://docs.djangoproject.com/
* https://getblimp.github.io/django-rest-framework-jwt/
* https://www.django-rest-framework.org/

Demo
----

```bash
# create rsa keys 
./build-pki.sh
# build image and run containers
./podman-run.sh
# create admin user 
podman exec -it django-docker-registry-jwt \
  /usr/bin/entrypoint.sh python3 manage.py createsuperuser

# test your login
podman login 127.0.0.1:5000
# Password: 
# Login Succeeded
```

Api
---
```
curl --cacert ./pki/ca.crt -u admin https://127.0.0.1:8443/api/v1/
curl --cacert ./pki/ca.crt -u admin https://127.0.0.1:8443/api/v1/registries/ -X OPTIONS

# Register a docker unique "127.0.0.1:5000" registry name:
# the name MUST matches the registry service name
# REGISTRY_AUTH_TOKEN_SERVICE="127.0.0.1:5000"
curl --cacert ./pki/ca.crt -u admin \
  https://127.0.0.1:8443/api/v1/registries/ \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"127.0.0.1:5000"}'
# {"id":1,"name":"127.0.0.1:5000"}

# register image 127.0.0.1:5000/django-test
curl --cacert ./pki/ca.crt -u admin \
  https://127.0.0.1:8443/api/v1/images/ \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"registry":"127.0.0.1:5000", "name":"django-test", "comment":"Simple PoC"}'
# {"registry":"127.0.0.1:5000","name":"django-test","comment":"Simple PoC","owner":"admin"}

# allow 'admin' user to push and pull into that container
# identified by name **service_name/image**
curl --cacert ./pki/ca.crt -u admin \
  https://127.0.0.1:8443/api/v1/permissions/ \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"image":"127.0.0.1:5000/django-test", "user":"admin", "pull":true, "push":true}'
# {"id":1,"image":"127.0.0.1:5000/django-test","user":"admin","push":true,"pull":true}

podman push 127.0.0.1:5000/django-test
# Getting image source signatures
# Copying blob cfceaafb5a19 done
# Copying blob 18f589330a95 done
# Copying config ab412d05a8 done
# Writing manifest to image destination
# Storing signatures
```

Tests
-----

TODO
