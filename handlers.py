from __future__ import unicode_literals
from datetime import datetime
import importlib

import jwt

def jwt_encode_kid_handler(payload):
    #from rest_framework_jwt.jwt_auth import settings
    from rest_framework_jwt.settings import api_settings as settings

    from django.conf import settings as dsettings
    
    kwargs = {
        'algorithm': settings.JWT_ALGORITHM
    } 
    
    # settings.JWT_AUTH_HEADER_KID is a custom variable
    # do not search JWT_AUTH_HEADER_KID in documentation
    if dsettings.JWT_AUTH_HEADER_KID: 
        kwargs['headers'] = {
            'kid': dsettings.JWT_AUTH_HEADER_KID
        }
    return jwt.encode(
        payload,
        settings.JWT_PRIVATE_KEY,
        **kwargs
    ).decode('utf-8')

