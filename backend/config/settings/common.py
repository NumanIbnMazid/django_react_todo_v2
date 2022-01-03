""" # Project Common Settings # """
from pathlib import Path
import os
import environ

""" *** Project Directory Configurations *** """
PosixPath_BASE_DIR = Path(__file__).resolve().parent.parent.parent
# BASE_DIR = environ.Path(__file__) - 3

# two folders back (/a/b/ - 2 = /)
root = environ.Path(__file__) - 3
# default location of .env file
DEFAULT_ENV_PATH = environ.Path(__file__) - 4
DEFAULT_ENV_FILE = DEFAULT_ENV_PATH.path('.env')()
# set default values and casting
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(env.str('ENV_PATH', DEFAULT_ENV_FILE))  # reading .env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()

""" *** Application Definitions *** """
THIRD_PARTY_APPS = [
    # Django Rest Framework
    "rest_framework",
    # Django Corsheaders
    "corsheaders",
]

LOCAL_APPS = [
    "todos",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
] + THIRD_PARTY_APPS + LOCAL_APPS


""" *** Middlewares Definitions *** """
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Django Whitenoise Middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Django Corsheader Middleware
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

""" *** Template Definitions *** """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

""" *** Authentication Configurations *** """
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


""" *** Localization Configuration *** """
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" *** Other Definitions *** """
SITE_ID = 1
WSGI_APPLICATION = 'config.wsgi.application'
# ASGI_APPLICATION = "config.routing.application"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
HOME_URL = "/"
ADMIN_LOGIN_URL = "/admin/login"
LOGIN_URL = ADMIN_LOGIN_URL

# Session Cookie Age
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # One month

""" # Project Third Party Packages Configurations # """

"""
----------------------- * Rest Framework Configuration * -----------------------
"""

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    #     # 'rest_framework.authentication.TokenAuthentication',
    # ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'utils.custom_exception_handler.custom_exception',
}

"""
----------------------- * Django Corsheaders Configuration * -----------------------
"""

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3000/'
# ]

CORS_ALLOW_ALL_ORIGINS = True