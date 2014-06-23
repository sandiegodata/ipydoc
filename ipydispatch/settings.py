"""
Django settings for ipydispatch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import abspath, dirname, basename, join


ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!


# Generate a new SECRET_KEY the first time the application is run.
try:
    from secret_key import *
except ImportError:
    SETTINGS_DIR=os.path.abspath(os.path.dirname(__file__))

    from django.utils.crypto import get_random_string
    import string
    import os

    with open(os.path.join(os.path.dirname(__file__), 'secret_key.py'),'w') as f:
        f.write("SECRET_KEY ='{}'".format(get_random_string(50,
                'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')))

    from secret_key import *


if False: # Set to True for debugging

    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['sandieodata.org', '127.0.0.1']

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_auth'
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.OpenIDBackend',
    'social_auth.backends.contrib.github.GithubBackend',
)

ROOT_URLCONF = 'ipydispatch.urls'

WSGI_APPLICATION = 'ipydispatch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'application.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'ipydispatch': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'views': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'any': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}


## Social Auth 
LOGIN_REDIRECT_URL = '/done'

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.assoc iate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'dispatcher.authpipe.create_user', # Previously 'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

GITHUB_APP_ID = '06fa28aa9d43c1f89d54'
GITHUB_API_SECRET = '2d5ee034234a079d810604491261f610b00e3487'

GITHUB_EXTENDED_PERMISSIONS = ['public_repo', 'gist', 'read:org', 'user:email']

