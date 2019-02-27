from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken

from datetime import datetime, timedelta

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def get_registry_scope(scope, user=None):
    """
    calculate from scope=repository:samalba/my-app:pull,push
        "access": [
        {
            "type": "repository",
            "name": "samalba/my-app",
            "actions": [
                "pull",
                "push"
            ]
        }
    
    access
        An array of access entry objects with the following fields:
    type
        The type of resource hosted by the service.
    name
        The name of the resource of the given type hosted by the service.
    actions
        An array of strings which give the actions authorized on this resource.
    
    """
    if scope:
        # FIXME: if scope is not a solid check
        # scope=repository:samalba/my-app:pull,push
        repos = scope.split(' ')
    else:
        repos = []
    print(repos)
    ret = []
    for r in repos:
        args = r.split(':')
        assert len(args) == 3
        actions = args[2].split(',')
        # FIXME: verify user's perms pull, push ...
        acc = { 
            'type': args[0],
            'name': args[1],
            'actions': actions
        }
        ret.append(acc)
    return ret

def jwt_docker_payload_handler(request):
    """
    Docker registry Claim Set
    https://docs.docker.com/registry/spec/auth/jwt/
    """
    query_params = request.query_params
    if request.user.is_active:
        # the user is active
        username = request.user.login
    else:
        # FIXME: check django.contrib.auth.models.AnonymousUser
        username = ""
    # https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
    timestamp = datetime.utcnow()
    payload = {
        # iss (Issuer)
        # The issuer of the token, typically the fqdn of the authorization server.
        'iss': "127.0.0.1",
        # sub (Subject)
        # The subject of the token; the name or id of the client which requested it. 
        # This should be empty (`""`) if the client did not authenticate.
        'sub': username,
        # aud (Audience)
        # The intended audience of the token; the name or id of the service which will verify the token to authorize the client/subject.
        'aud': query_params.get('service'),
        # exp (Expiration)
        # The token should only be considered valid up to this specified date and time.
        'exp': timestamp + api_settings.JWT_EXPIRATION_DELTA,
        # nbf (Not Before)
        # The token should not be considered valid before this specified date and time.
        'nbf': timestamp,
        # iat (Issued At)
        # Specifies the date and time which the Authorization server generated this token.
        'iat': timestamp,
        # jti (JWT ID)
        # A unique identifier for this token. Can be used by the intended audience to prevent replays of the token.
        'jit': 'FIXME' + str(timestamp),
    }
    
    access = get_registry_scope(query_params.get('scope',''), user=request.user)
    payload['access'] = access

    # if api_settings.JWT_AUDIENCE is not None:
    #    payload['aud'] = api_settings.JWT_AUDIENCE

    # if api_settings.JWT_ISSUER is not None:
    #    payload['iss'] = api_settings.JWT_ISSUER

    return payload

class DockerObtainJSONWebToken(ObtainJSONWebToken):
    """
    django rest framework jwt implementation for docker registry
    https://docs.docker.com/registry/spec/auth/jwt/
    """
    def get(self, request, *args, **kwargs):
        # read query parameters 
        # example : https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
        data = request.query_params.copy()
        # After authenticating the client 
        # (which may simply be an anonymous client if no attempt was made to authenticate), 
        # the token server must next query its access control list to determine whether 
        # the client has the requested scope.
        # If the request is unauthenticated the default value of request.user 
        # is an instance of django.contrib.auth.models.AnonymousUser.
        user = request.user
        print(data, user)

        payload = jwt_docker_payload_handler(request)
        token = jwt_encode_handler(payload)
        print(token, payload)
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        return response
        # serializer = self.get_serializer(data=data)
        

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

docker_obtain_jwt_token = DockerObtainJSONWebToken.as_view()
