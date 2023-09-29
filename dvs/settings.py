

from pathlib import Path
import pytz
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '8f3a591832383b7572bf36afb857010335f7cfbbcba42129596bc7b6b4c180b9f2214d8b19a4b3567d0cea924d0f76fa96cd8c6a6b9c174c230e9396aa65c67e'


ALLOWED_HOSTS = ['*']
DOMAIN_HOST = ['*']
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://localhost:3000']

APPEND_SLASH = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_onboarding',
    'pms',
    'rest_framework',
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware'
]

RATELIMIT_VIEW='dvs.views.ratelimitingview'

ROOT_URLCONF = 'dvs.urls'

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'custompms': 'pms.custom',
            }
        },
    },
]

WSGI_APPLICATION = 'dvs.wsgi.application'

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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

IST = pytz.timezone('Asia/Kolkata')

USE_I18N = True
USE_L10N = True
USE_TZ = True

START_TIME = '00:00:00'
END_TIME = '23:59:59'


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/api/pms/v1/home/'
LOGOUT_REDIRECT_URL = '/'
CORS_ALLOW_ALL_ORIGINS = True

AUTHENTICATED_RATE_LIMIT = '500/m'
UNAUTHENTICATED_RATE_LIMIT = '100/m'

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587


file = open('secretes.json')
data = json.load(file)
file.close()

CURRENT_ENV = os.getenv('ENV')

if CURRENT_ENV == "PROD":
    DATABASES = data['DATABASES_PROD'] #POSTGRESQL
    EMAIL_HOST_USER = data['GMAIL_PROD']['GMAIL_USER']
    EMAIL_HOST_PASSWORD = data['GMAIL_PROD']['GMAIL_PASSWORD']
    AUTH = data["2FA_AUTH_PROD"]
    DEBUG = False
else:
    DATABASES = data['DATABASES_LOCAL'] #SQLITE
    EMAIL_HOST_USER = data['GMAIL_LOCAL']['GMAIL_USER']
    EMAIL_HOST_PASSWORD = data['GMAIL_LOCAL']['GMAIL_PASSWORD']
    AUTH = data["2FA_AUTH_LOCAL"]
    DEBUG = True