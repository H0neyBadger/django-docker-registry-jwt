curl -L -O https://storage.googleapis.com/kubernetes-release/easy-rsa/easy-rsa.tar.gz
tar xzf easy-rsa.tar.gz
pushd easy-rsa-master/easyrsa3
export EASYRSA_ALGO=ec
export EASYRSA_CURVE="P-256"
./easyrsa init-pki
MASTER_IP="django-docker-registry-jwt"
MASTER_IP="127.0.0.1"
./easyrsa --batch "--req-cn=${MASTER_IP}@`date +%s`" build-ca nopass
./easyrsa --subject-alt-name="IP:${MASTER_IP}" build-server-full server nopass
popd
cat ./easy-rsa-master/easyrsa3/pki/ca.crt \
    ./easy-rsa-master/easyrsa3/pki/issued/server.crt \
    > ./easy-rsa-master/easyrsa3/pki/ca_bundle.crt

sudo chcon -t container_file_t ./easy-rsa-master/easyrsa3/pki/ca_bundle.crt
