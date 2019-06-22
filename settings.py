"""
User defined configuration file
"""

# SECURITY WARNING: keep the secret key used in production secret!
# ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
SECRET_KEY = 'CHANGE_ME'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# disable browsable api 
# REST_FRAMEWORK = getattr(default_settings,"REST_FRAMEWORK", {})
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']= ( 'rest_framework.renderers.JSONRenderer', )

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = 'static/'

# FIXME: allow key path settings
# JWT_EC_CERT_PATH = './pki/issued/token.crt'
# JWT_EC_PRIVATE_KEY_PATH = './pki/private/token.key'


