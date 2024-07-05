import os

from .general import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'info@mavericksbank.com'
