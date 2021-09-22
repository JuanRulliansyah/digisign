import os
from datetime import timedelta

from gramedia.common.env import EnvConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = EnvConfig(app_prefix='KA')

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-_sfu%e)wm!b1cdtekp4_=_$p4&e66#b_%(&t$9lx8@%btdke7&'
SECRET_KEY = config.string('SECRET_KEY', 'dsdevkey')
DEBUG = config.boolean('DEBUG', True)
ALLOWED_HOSTS = config.string('ALLOWED_HOSTS', '*').split(',')
FORCE_SCRIPT_NAME = config.string('FORCE_SCRIPT_NAME', '/api/digisign')
CORS_ALLOW_ALL_ORIGINS = config.boolean('CORS_ALLOW_ALL_ORIGINS', True)
CORS_ALLOWED_ORIGINS = config.string('CORS_ALLOWED_ORIGINS').split(',') if config.string('CORS_ALLOWED_ORIGINS') else []
CORS_EXPOSE_HEADERS = [
    'X-Page',
    'X-Page-Size',
    'X-Total-Results',
    'Link',
    'Location',
    'ETag',
    'Last-Modified',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'x-user-agent',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'if-none-match',
    'if-modified-since',
    'cache-control',
    'content-type',
    'range',
]
# DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'rest_framework',

    'digisign.auth.apps.AuthConfig',
    'digisign.users.apps.UsersConfig',
    'digisign.modules.apps.ModulesConfig',
    'digisign.access_groups.apps.AccessGroupsConfig',
    'digisign.documents.apps.DocumentsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'users.User'
ROOT_URLCONF = 'digisign.urls'
WSGI_APPLICATION = 'digisign.wsgi.application'
SITE_ID = 1
MUTE_SIGNALS = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

DATABASES = {
    'default': config.django_db('DB_PRIMARY', 'postgresql://dev:dev@127.0.0.1:5432/digisign'),
    'replica': config.django_db('DB_REPLICA', 'postgresql://dev:dev@127.0.0.1:5432/digisign')
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = f'{FORCE_SCRIPT_NAME}/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media
MEDIA_URL = f'{FORCE_SCRIPT_NAME}/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Rest Framework
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'kitchenart.drf.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'login_attempts': '15/hr',
        'user': '60/min',
    },
    'DEFAULT_PAGINATION_CLASS': 'kitchenart.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 25,
    'SEARCH_PARAM': 'q',
    'URL_FIELD_NAME': 'href'
}

# Configure JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ISSUER': 'digisign',
    'USER_ID_FIELD': 'username'
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CERTIFICATE_PATH = BASE_DIR + '/credentials/certificates/localhost.p12'
PASSWORD = 'passpass'
DIGEST = 'sha512'
MAX_UPLOAD_SIZE = 10485760