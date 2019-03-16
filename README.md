Django rest jwt for docker registry 
===================================

Simple rest api to handle docker registy v2 authorizations

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
```

Api
---
```
curl --cacert ./pki/ca.crt -u admin https://127.0.0.1:8443/api/v1/
curl --cacert ./pki/ca.crt -u admin https://127.0.0.1:8443/api/v1/registries/ -X OPTIONS
```

Tests
-----

TODO
