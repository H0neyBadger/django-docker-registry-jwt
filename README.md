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
sudo docker-compose up -d
# create/update database schema
sudo docker-compose exec web python3 manage.py migrate
# create admin user 
sudo docker-compose exec web python3 manage.py createsuperuser

# test your login
sudo docker login 127.0.0.1:5000
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

sudo docker push 127.0.0.1:5000/django-test
# The push refers to a repository [127.0.0.1:5000/django-test]
# bbc38b3303a7: Pushed 
# b1c0701756b0: Pushed 
# 7a74c09822ff: Pushed 
# e5f269580026: Pushed 
# b634b7704ba0: Pushed 
# b7ba3be6a0d6: Pushed 
# latest: digest: sha256:702ce186a611ec776dda9faf8683e37a24a121f653885d1ee52f9fcf1297f3e7 size: 1582
```

Tests
-----

TODO
