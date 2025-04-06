from .common import *
from .partials.util import get_secret

DEBUG = True
DEBUG_TOOLBAR = True

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

ALLOWED_HOSTS = ['https://chilasi.asidigital.co', '*']
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
BASE_URL = 'https://chilasi.asidigital.co'

# ADMINS (For error notifications)
ADMINS = [
    ('Edwin', 'edwinmoreno328@gmail.com'),
]


PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": os.environ.get('FCM_API_KEY', ''),
    # "APNS_CERTIFICATE": "./certs/aps-dev.pem",
    "APNS_AUTH_KEY_PATH": os.environ.get('APNS_AUTH_KEY_PATH', ''),
    "APNS_AUTH_KEY_ID": os.environ.get('APNS_AUTH_KEY_ID', ''),
    "APNS_TEAM_ID": os.environ.get('APNS_TEAM_ID', ''),
    "APNS_TOPIC": os.environ.get('APNS_TOPIC', ''),
    "APNS_USE_SANDBOX": False,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

SOCKET_SERVICE_URL = os.environ.get('SOCKET_SERVICE_URL', '')


if get_secret('DATABASE_URL'):
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config()
    }
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
else:
    POSTGRES_USER = get_secret('POSTGRES_USER')
    POSTGRES_PASSWORD = get_secret('POSTGRES_PASSWORD')

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'project_name',
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'db',
            'PORT': 5432,
        }
    }
# Simple JWT
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    'SIGNING_KEY': SECRET_KEY,
})

# Email Config
"""
EMAIL_PASSWORD = get_secret('EMAIL_PASSWORD')
EMAIL_HOST = 'smtp.asi-backend.com'
EMAIL_HOST_USER = 'asi-backend'
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
"""

SPECTACULAR_SETTINGS['SERVERS'] = [{"url": "https://chilasi.asidigital.co"}]

API_FIREBASE_KEY = os.environ.get('API_FIREBASE_KEY', '')
PASSWORD_RESET_EXPIRE_DAYS = 1



CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),  # Usa la variable de entorno
    }
}
