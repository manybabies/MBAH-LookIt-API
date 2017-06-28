"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.contrib.messages import constants as messages
import raven

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c*si4oji5r=#)5+6e$bi@an%v)(n2be2+1(s985uh4mu3jq!qt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = [h for h in os.environ.get('ALLOWED_HOSTS', '').split(' ') if h]

AUTH_USER_MODEL = 'accounts.User'
GUARDIAN_MONKEY_PATCH = False

# S3 Bucket name where video attachments are stored
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'fakeBucketName')

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',

    # third-party
    'django_extensions',
    'guardian',
    'localflavor',
    'rest_framework',
    'bootstrap3',
    'debug_toolbar',
    'ace_overlay',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_json_api',
    'storages',

    # our stuff
    'osf_oauth2_adapter',
    'api',
    'web',
    'accounts',
    'studies',
    'exp',

    # at the bottom so overriding form widget templates have a fallback
    'django.forms',
    'django.contrib.admin',

    # at the bottom so overriding templates is possible
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]
if not DEBUG:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
    RAVEN_CONFIG = {
        'dsn': os.environ.get('RAVEN_DSN', None),
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        'release': os.environ.get('GIT_COMMIT', 'No version'),
    }


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1', ]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'project.urls'
LOGIN_URL = '/login/'
EXPERIMENTER_LOGIN_URL = '/accounts/login/'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['django/forms/templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.postgresql',  # django.db.backends.postgresql
        'NAME': os.environ.get('DB_NAME', 'lookit'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'api.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'api.renderers.JSONAPIRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
    }

JSON_API_FORMAT_KEYS = 'dasherize'
JSON_API_PLURALIZE_TYPES = True

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'localhost:8000')
SITE_NAME = os.environ.get('SITE_NAME', 'Lookit')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# base url for experiments, should be s3 bucket in prod
EXPERIMENT_BASE_URL = os.environ.get('EXPERIMENT_BASE_URL', 'http://google.com/')  # default to ember base url
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')  # default to ember base url

LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL', 'http://localhost:8000/exp/')
ACCOUNT_LOGOUT_REDIRECT_URL = os.environ.get('ACCOUNT_LOGOUT_REDIRECT_URL', '/api/')
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
SOCIALACCOUNT_ADAPTER = 'osf_oauth2_adapter.views.OSFOAuth2Adapter'
SOCIALACCOUNT_PROVIDERS = \
    {'osf':
        {
            'METHOD': 'oauth2',
            'SCOPE': ['osf.users.email_read', 'osf.users.profile_read', ],
            'AUTH_PARAMS': {'access_type': 'offline'},
            # 'FIELDS': [
            #     'id',
            #     'email',
            #     'name',
            #     'first_name',
            #     'last_name',
            #     'verified',
            #     'locale',
            #     'timezone',
            #     'link',
            #     'gender',
            #     'updated_time'],
            # 'EXCHANGE_TOKEN': True,
            # 'LOCALE_FUNC': 'path.to.callable',
            # 'VERIFIED_EMAIL': False,
            # 'VERSION': 'v2.4'
        }
     }


# Configuration for cross-site requests
CORS_ORIGIN_ALLOW_ALL = True  # TODO Needs to be changed before production!
CORS_ORIGIN_WHITELIST = ()

if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    # if we're trying to use cloud storage
    STATICFILES_LOCATION = '/static'
    STATICFILES_STORAGE = 'project.storages.LookitStaticStorage'
    STATIC_URL = os.environ.get('STATIC_URL', 'https://storage.googleapis.com/io-osf-lookit-staging2/static/')

    MEDIAFILES_LOCATION = '/media'
    DEFAULT_FILE_STORAGE = 'project.storages.LookitMediaStorage'
    MEDIA_URL = os.environ.get('MEDIA_URL', 'https://storage.googleapis.com/io-osf-lookit-staging2/media/')

    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME', 'io-osf-lookit-staging2')
    GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID', 'cos-staging')
else:
    # we know nothing about cloud storage
    print('-------------------Why yes, we are using local assets!-------------------------')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'D4nkM3m35C4n')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'M31tSt331B34m5')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_FROM_ADDRESS = os.environ.get('EMAIL_FROM_ADDRESS', 'lookit.robot@some.domain')
EMAIL_BACKEND = f"django.core.mail.backends.{'smtp' if not DEBUG else 'console'}.EmailBackend"
# disable smtp backend for now
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# United States will show up first in the countries list on the Demographic Data form
COUNTRIES_FIRST=['US']

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
EMBER_EXP_PLAYER_REPO = 'https://github.com/pattisdr/ember-frame-player'
EMBER_ADDONS_REPO = 'https://github.com/centerforopenscience/exp-addons'
