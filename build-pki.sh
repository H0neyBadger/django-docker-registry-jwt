curl -L -O https://storage.googleapis.com/kubernetes-release/easy-rsa/easy-rsa.tar.gz
tar xzf easy-rsa.tar.gz
pushd easy-rsa-master/easyrsa3
./easyrsa init-pki
MASTER_IP="django-docker-registry-jwt"
MASTER_IP="127.0.0.1"
./easyrsa --batch "--req-cn=${MASTER_IP}@`date +%s`" build-ca nopass
./easyrsa --subject-alt-name="IP:${MASTER_IP}" build-server-full server nopass

