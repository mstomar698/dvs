

from pathlib import Path
import pytz
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '8f3a591832383b7572bf36afb857010335f7cfbbcba42129596bc7b6b4c180b9f2214d8b19a4b3567d0cea924d0f76fa96cd8c6a6b9c174c230e9396aa65c67e'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['*']
DOMAIN_HOST = "https://s2analytica.suvidhaen.org"
CSRF_TRUSTED_ORIGINS = [
    'https://s2analytica.suvidhaen.org', 'http://s2analytica.suvidhaen.org','https://s2analytica.suvidhaen.com', 'http://s2analytica.suvidhaen.com']

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
    'railmadad',
    'cmm',
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
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'RatelimitMiddleware.middleware.RatelimitMiddleware'
]

RATELIMIT_VIEW='s2analytica.views.ratelimitingview'

ROOT_URLCONF = 's2analytica.urls'

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
                'customrailmadad': 'railmadad.custom',
                'customcmm': 'cmm.custom',

            }
        },
    },
]

# WSGI_APPLICATION = 's2analytica.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

IST = pytz.timezone('Asia/Kolkata')

USE_I18N = True
USE_L10N = True
USE_TZ = True

START_TIME = '00:00:00'
END_TIME = '23:59:59'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/api/pms/v1/home/'
LOGOUT_REDIRECT_URL = '/'
CORS_ALLOW_ALL_ORIGINS = True

AUTHENTICATED_RATE_LIMIT = '50/m'
UNAUTHENTICATED_RATE_LIMIT = '10/m'

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587


file = open('secretes.json')
data = json.load(file)
file.close()

CURRENT_ENV = os.getenv('ENV')

if CURRENT_ENV == "PROD":
    EMAIL_HOST_USER = data['GMAIL_PROD']['GMAIL_USER']
    EMAIL_HOST_PASSWORD = data['GMAIL_PROD']['GMAIL_PASSWORD']
    DATABASES = data['DATABASES_PROD']
    AUTH = data["2FA_AUTH_PROD"]
    DEBUG = True
else:
    EMAIL_HOST_USER = data['GMAIL_LOCAL']['GMAIL_USER']
    EMAIL_HOST_PASSWORD = data['GMAIL_LOCAL']['GMAIL_PASSWORD']
    DATABASES = data['DATABASES_LOCAL']
    AUTH = data["2FA_AUTH_LOCAL"]
    DEBUG = True


CMM__DRIVE_FOLDER_ID = data['DRIVE']['CMM__DRIVE_FOLDER_ID']
RAILMADAD__DRIVE_FOLDER_ID = data['DRIVE']['RAILMADAD__DRIVE_FOLDER_ID']

SERVICE_ACCOUNT_FILE = data['DRIVE']['SERVICE_ACCOUNT_FILE_NAME']

DEBUG = True