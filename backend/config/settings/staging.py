""" # Development Environment Configurations # """
# import common configurations
from config.settings.common import *
import dj_database_url

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(" ")

""" *** Application Secret Key *** """
SECRET_KEY = env('SECRET_KEY', default=None)

""" *** DEBUG Configurations *** """
DEBUG = env('DEBUG', default=True)

ROOT_URLCONF = 'config.urls'

""" *** Database Configuration *** """
try:
    if env('DEVELOPMENT_DATABASE_URL', default=None):
        DATABASE_URL = env('DEVELOPMENT_DATABASE_URL')
    elif env('DATABASE_URL', default=None):
        DATABASE_URL = env('DATABASE_URL')
    else:
        try:
            DATABASE_URL = f"postgres://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT', cast=int)}/{env('DB_NAME')}"
        except Exception as E:
            print("Exception::=> ", E)
            DATABASE_URL = 'sqlite:///' + \
                os.path.join(PosixPath_BASE_DIR, 'db.sqlite3')

    # Define DATABASES
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
except Exception as E:
    print("Exception::=> ", E)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': PosixPath_BASE_DIR / 'db.sqlite3',
        }
    }

TEMPLATES[0]["DIRS"] = [os.path.join(PosixPath_BASE_DIR, 'templates')]

""" *** Static & Media Files Configurations *** """
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(PosixPath_BASE_DIR, 'staticfiles'),
]

STATIC_ROOT = os.path.join(PosixPath_BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(PosixPath_BASE_DIR, 'media/')
