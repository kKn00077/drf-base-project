from .base import *

DEBUG = False

ALLOWED_HOSTS = []

# TODO: DB 정보 변경
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}