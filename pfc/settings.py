"""
Django settings for pfc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['static'])
STATIC_URL = '/static/'

MEDIA_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['media'])
MEDIA_URL = '/media/'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('secret_key', None)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['geo.epseb.upc.edu']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'map',
    'south',
    'widget_tweaks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pfc.urls'

WSGI_APPLICATION = 'pfc.wsgi.application'

LOGIN_URL = '/back'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {'default': {}}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
DATABASES['default']['NAME'] = os.environ.get('db_name', None)
DATABASES['default']['USER'] = os.environ.get('db_user', None)
DATABASES['default']['PASSWORD'] = os.environ.get('db_password', None)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Mail configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('email_user', None)
EMAIL_HOST_PASSWORD = os.environ.get('email_password', None)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('server_email', None)
SERVER_EMAIL = os.environ.get('server_email', None)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOGGING
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'devel': {
            'format': 'DEVEL[%(levelname)s] %(message)s',
        },
        'basic': {
            'format': '%(message)s',
        },
        'time': {
            'format': '[%(asctime)s]  %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'devel'
        },
        'console_commands':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'basic'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
